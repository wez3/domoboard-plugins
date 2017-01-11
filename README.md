# Domoboard plugins

Domoboard is a dashboard for Domoticz based on Python Flask. The decision was made to use Domoticz as an backend because it is a powerful framework for home automation. Flask was choosen to get all the powerful features that Python offers.

This git repository contains all available plugins for Domoboard.

# Quick install

On the settings page Domoboard offers a tab which allows users to install plugins automatically. Using this page plugins from this GitHub page can be installed in just one click.

![alt tag](https://domoboard.nl/domoboard_images/domoboard_plugin_install.png)

# Manually install plugins

Clone this git.

```
git clone https://github.com/wez3/domoboard-plugins
```

Select the plugin that you wish to install. Navigate to the folder of the plugin and copy the plugin files in to the webroot of the Domoboard dashboard.

```
cd example-plugin
cp -r * /path/to/domoboard
```

Check the plugins README file (if available) to check whether special action are required to install the plugin.

# Keep in mind during development

- Make sure to use the requestAPI(url) JavaScript function which is builtin to Domoboard when calling the API. This function adds a Cross Site Request Forgery (CSRF) token to the request, which is required when calling the API.
