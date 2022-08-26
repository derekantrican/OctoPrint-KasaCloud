# OctoPrint-Kasacloud

A proof-of-concept plugin to turn on & off a TP-Link (Kasa) switch using the [cloud API](https://github.com/derekantrican/TP-Link-Python). This makes it possible to set the state of a switch even if it isn't accessible over the network (or is on a different network).

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html) using this URL:

    https://github.com/derekantrican/OctoPrint-Kasacloud/archive/master.zip

After installing, open OctoPrint settings, then go to "Plugins" > "KasaCloud Plugin". The instructions there will help you test it out.

The end goal of this proof-of-concept is to integrate this work into the more widely used [TP-Link Smartplug plugin](https://github.com/jneilliii/OctoPrint-TPLinkSmartplug).
