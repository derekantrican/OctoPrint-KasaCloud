# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import requests
import json

class KasaCloudPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SimpleApiPlugin
):

    EXPIRED_TOKEN_ERROR_CODE = -20651
    kasa_api_token = ''

    def get_kasa_api_token(self):
        url = 'https://wap.tplinkcloud.com'
        data = { 
            'method' : 'login',
            'params' : {
                'appType' : 'Kasa_Android',
                'cloudUserName' : self._settings.get(['email']),
                'cloudPassword' : self._settings.get(['password']),
                'terminalUUID' : '7218c95b-aa76-4654-8c9c-545466672961'
            }
        }

        response = requests.post(url, data = json.dumps(data))
        responseJson = json.loads(response.text)
        self.kasa_api_token = responseJson['result']['token']

    def get_devices(self):
        url = f'https://wap.tplinkcloud.com?token={self.kasa_api_token}'
        data = { 
            'method' : 'getDeviceList'
        }

        response = requests.post(url, data = json.dumps(data))
        responseJson = json.loads(response.text)
        return responseJson['result']['deviceList']

    def on_after_startup(self):
        self.get_kasa_api_token()
        self._logger.info(f"KasaCloud API Token: {self.kasa_api_token}")

    def set_device_state(self, state):
        devices = self.get_devices()

        self._logger.info(devices)
        self._logger.info(f"Looking for device with alias '{self._settings.get(['device_alias'])}'")

        matching_device = next((device for device in devices if device['alias'] == self._settings.get(['device_alias'])), None)

        if not matching_device:
            self._logger.info(f"Could not find a device with alias '{self._settings.get(['device_alias'])}'")
            raise Exception(f"Could not find a device with alias '{self._settings.get(['device_alias'])}'")

        self._logger.info(f"Setting state to {'on' if state else 'off'}")

        url = f'https://wap.tplinkcloud.com?token={self.kasa_api_token}'
        data = { 
            'method' : 'passthrough',
            'params' : {
                'deviceId' : matching_device['deviceId'],
                'requestData' : json.dumps({
                    'system' : {
                        'set_relay_state' : {
                            'state' : 1 if state else 0
                        }
                    }
                })
            }
        }

        response = requests.post(url, data = json.dumps(data))
        responseJson = json.loads(response.text)

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return {
            'email' : '',
            'password' : '',
            'device_alias' : ''
        }

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/KasaCloud.js"],
            "css": ["css/KasaCloud.css"]
        }

    ##~~ SettingsPlugin mixin

    def get_api_commands(self):
        return {
            'turnOn': [],
            'turnOff': []
        }

    def on_api_command(self, command, data):
        try:
            if command == 'turnOn':
                self.set_device_state(True)
            elif command == 'turnOff':
                self.set_device_state(False)
            
            return {
                'success' : True,
                'message' : 'Success!'
            }
        except Exception as e:
            self._logger.info(f"Exception thrown when trying to set device state: {e}")
            return {
                'success' : False,
                'message' : str(e)
            }


    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "KasaCloud": {
                "displayName": "KasaCloud Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "derekantrican",
                "repo": "OctoPrint-Kasacloud",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/derekantrican/OctoPrint-Kasacloud/archive/{target_version}.zip",
            }
        }


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "KasaCloud Plugin"


# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = KasaCloudPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
