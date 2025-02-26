# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "mobile_notification"
app_title = "Mobile Notification"
app_publisher = "Tridots Tech"
app_description = "App for sending One Signal Notifications from admin site"
app_icon = "octicon octicon-file-directory"
app_color = "blue"
app_email = "vigneshwaran@valiantsystems.com"
app_license = "MIT"
fixtures = [
	{
		"dt":"Custom Field",
		"filters":[["name","in",['Email Alert-send_mobile_notification',
		'Email Alert-mobile_notification_message']]]
	}
]
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/mobile_notification/css/mobile_notification.css"
# app_include_js = "/assets/mobile_notification/js/mobile_notification.js"

# include js, css files in header of web template
# web_include_css = "/assets/mobile_notification/css/mobile_notification.css"
# web_include_js = "/assets/mobile_notification/js/mobile_notification.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "mobile_notification.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "mobile_notification.install.before_install"
# after_install = "mobile_notification.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mobile_notification.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"mobile_notification.tasks.all"
# 	],
# 	"daily": [
# 		"mobile_notification.tasks.daily"
# 	],
# 	"hourly": [
# 		"mobile_notification.tasks.hourly"
# 	],
# 	"weekly": [
# 		"mobile_notification.tasks.weekly"
# 	]
# 	"monthly": [
# 		"mobile_notification.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "mobile_notification.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "mobile_notification.event.get_events"
# }

