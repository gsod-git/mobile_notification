# -*- coding: utf-8 -*-
# Copyright (c) 2018, Tridots Tech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate
from datetime import date,datetime
import json
from requests.exceptions import HTTPError
from onesignalclient.app_client import OneSignalAppClient
from onesignalclient.notification import Notification

class AppNotificationCenter(Document):
	pass	

@frappe.whitelist()
def insert_notification(name,message,table_5,url=None):	
	frappe.get_doc({
		"doctype": "Notification",
        "name": get_random(),
        "notification_name":name,
        "message":message,
        "url":url
		}).insert()
	notification=frappe.get_last_doc('Notification')
	responsedata=json.loads(table_5)	
	for item in responsedata:
		frappe.get_doc({
			"doctype":"Member Notification List",
			"parent":notification.name,
			"parenttype":"Notification",
			"parentfield":"table_5",
			"member":item.get('member'),
			"member_name":item.get('member_name')
			}).insert()

@frappe.whitelist()
def get_random():
	import random 
	import string
	random = ''.join([random.choice(string.ascii_letters
            + string.digits) for n in range(6)])
	Name=frappe.db.get_all('Notification',fields=['name'])
	for x in Name:
		if x.name==random:
			random=get_random()
	return random
@frappe.whitelist()
def get_items(url):
	now=getdate(nowdate())
	if frappe.db.get_value("DocType", url):
		if url=='Events':
			data=frappe.db.sql('''select name from `tabEvents` where start_date>=%(now)s''',{'now':nowdate()},as_dict=1)
			return data
		elif url=='Samaj Darshan':
			data=frappe.db.get_all('Samaj Darshan',fields=['name','year'],filters={'year':now.year})
			for item in data:
				item.list=frappe.db.get_all('Samaj Darshan Lists',fields=['*'],filters={'parent':item.name,'published':0})
			return data
		else:
			data=frappe.db.get_all(url,fields=['*'])
			return data
@frappe.whitelist()
def send_notification(doctype,docname,message,subject):
	app_notification_settings=frappe.get_single('App Notification Settings')
	doc=frappe.get_doc(doctype,docname)
	if doc.member:
		member=frappe.get_doc('Member',doc.member)
		if member.player_id:	
			player_id = member.player_id
			os_app_id = app_notification_settings.app_id
			os_apikey = app_notification_settings.secret_key

			# Init the client
			client = OneSignalAppClient(app_id=os_app_id, app_api_key=os_apikey)

			# Creates a new notification
			notification = Notification(app_notification_settings.app_id, Notification.DEVICES_MODE)
			notification.include_player_ids = [player_id]  # Must be a list!
			notification.data={'add_data':message}
			notification.contents={"en":subject}
			try:
			    # Sends it!
			    result = client.create_notification(notification)
			    frappe.get_doc({"doctype": "Notification","name": get_random(),"notification_name":subject,
        			"message":message}).insert()
			    last_notification=frappe.get_last_doc('Notification')
			    frappe.get_doc({"doctype":"Member Notification List","parent":last_notification.name,
					"parenttype":"Notification","parentfield":"table_5","member":member.name,
					"member_name":member.member_name}).insert()
			except HTTPError as e:
			    result = e.response.json()
			print(result)