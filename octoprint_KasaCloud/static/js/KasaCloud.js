/*
 * View model for OctoPrint-Kasacloud
 *
 * Author: Derek Antrican
 * License: AGPLv3
 */
$(function() {
    function KasaCloudViewModel(parameters) {
        var self = this;

        // self.settings = parameters[0].settings.plugins.KasaCloud;
        self.settings = parameters[0];

        // self.startupComplete = ko.observable(false);

        // self.email = ko.computed(() =>
        //     self.startupComplete() ? self.settings.email : ""
        // );

        // self.email = ko.computed({
		// 	read: () => self.startupComplete() && self.settings.email(),
		// 	write: em => self.startupComplete() && self.settings.email(em),
		// });

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        // TODO: Implement your plugin's view model here.

        // self.events = ko.computed(() =>
        //     self.startupComplete() ? self.settings.events() : []
        // );

        // self.onStartupComplete = () => {
        //     // console.log("%c=== KasaCloud startup complete ===", "color: green");
        //     // console.log(parameters[0].settings.plugins);
		// 	self.settings = parameters[0].settings.plugins.KasaCloud;
		// 	// self.startupComplete(true);
		// 	// console.log(self.settings.events(), self.events());
		// }

        self.turnOn = function(data) {
            console.log("Turning on");
			$.ajax({
			url: API_BASEURL + "plugin/KasaCloud",
			type: "POST",
			dataType: "json",
			data: JSON.stringify({
				command: "turnOn"
			}),
			contentType: "application/json; charset=UTF-8"
			});		
		}

        self.turnOff = function(data) {
            console.log("Turning off");
			$.ajax({
			url: API_BASEURL + "plugin/KasaCloud",
			type: "POST",
			dataType: "json",
			data: JSON.stringify({
				command: "turnOff"
			}),
			contentType: "application/json; charset=UTF-8"
			});		
		}
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: KasaCloudViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ /* "loginStateViewModel",*/ "settingsViewModel" ],
        // Elements to bind to, e.g. #settings_plugin_KasaCloud, #tab_plugin_KasaCloud, ...
        elements: [ "#settings_plugin_KasaCloud" ]
    });
});
