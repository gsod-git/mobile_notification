# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		# {
		# 	"module_name": "Mobile Notification",
		# 	"color": "#bdc3c7",
		# 	"icon": "octicon octicon-file-directory",
		# 	"type": "module",
		# 	"label": _("Mobile Notification")
		# },
		{
			"module_name": "App Notification",
			"color": "#bdc3c7",
			"reverse": 1,
			"icon": "octicon octicon-settings",
			"type": "module",
			"hidden": 1
		},		
	]
