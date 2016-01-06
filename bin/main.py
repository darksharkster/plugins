#!/bin/python

import os
import sys
sys.path.append(os.getcwd())

import plugin_loader

if __name__ == "__main__":
	plugins = plugin_loader.enumerate_plugins("/home/seanmcg/src/python/modules/plugins")
	for plugin in plugins:
		print "plugin is:", plugin
