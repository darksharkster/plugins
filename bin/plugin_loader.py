import imp
import os.path
import re
import sys

def plugin_description(path):
	good_file = (os.path.isfile(path) and path.endswith('.py')
		and not path.startswith('_'))
	good_dir = (os.path.isdir(path) and
		os.path.isfile(os.path.join(path, '__init__.py')))
	if good_file:
		name = os.path.basename(path)[:-3]
		return (name, path, imp.PY_SOURCE)
	elif good_dir:
		name = os.path.basename(path)
		return (name, path, imp.PKG_DIRECTORY)
	else:
		return None

def _update_plugins_from_dir(plugins, directory):
	for path in os.listdir(directory):
		path = os.path.join(directory, path)
		plugin_desc = plugin_description(path)
		if plugin_desc:
			plugins[plugin_desc[0]] = plugin_desc[1:]

def enumerate_plugins(plugins_dir):
	""" Return a dict mapping the names of plugins to a tuple of the plugin name """
	plugins = {}
	_update_plugins_from_dir(plugins, plugins_dir)
	return plugins

def load_plugin(name, path, type_):
	if type__ == imp.PY_SOURCE:
		with open(path) as plugin_file:
			plugin = imp.load_module(name, plugin_file, path, ('.py', 'U', type_))
	elif type__ == imp.PKG_DIRECTORY:
		plugin = imp.load_module(name, None, path, ('', '', type_))
	else:
		raise TypeError('Unsupported plugin type')

	return plugin, os.path.getmtime(path)
