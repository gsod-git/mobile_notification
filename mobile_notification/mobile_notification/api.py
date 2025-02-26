# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, cstr
from frappe.email.doctype.email_group.email_group import add_subscribers
from frappe.utils import getdate,datetime,nowdate,today
from datetime import date

@frappe.whitelist(allow_guest=True)
def get_aboutus_settings():
	aboutus = frappe.db.get_single_value('About Us Settings', 'company_introduction')
	return aboutus
@frappe.whitelist(allow_guest=True)
def get_general_settings():
	settings = frappe.get_single('General Settings')
	return settings

@frappe.whitelist(allow_guest=True)
def get_search_result(txt):

	# return frappe.db.sql('''select name as name,membership_type as membership_type,gender as gender,active as active,last_name as last_name,membership_expiry_date as membership_expiry_date,date_of_birth as date_of_birth,image as image,address_line_1 as address_line_1,city as city,zip_code as zip_code,state as state,newsletter as newsletter,address_line_2 as address_line_2,member_name as member_name,phone_no as phone_no,email as email from `tabMember`
	# 		where phone_no like %(txt)s or member_name like %(txt)s or email like %(txt)s order by member_name'''.format(), {
	# 				"txt": "%{0}%".format(txt),
	# 				"_txt": txt.replace('%', '')
	# 		})
	# return frappe.get_all("Member", fields=["*"], filters = [["phone_no","like","%"+txt+"%"],["member_name","like", "%"+txt+"%"]])
	return frappe.get_all("Member", fields=["*"], filters = {"member_name": ("like", "%"+txt+"%"), "active" : ("=","1")})
	# 
@frappe.whitelist(allow_guest=True)
def get_eventsearch_result(txt):
	now=getdate(nowdate())
	return frappe.get_all("Events", fields=["*"], filters = {"name1": ("like", "%"+txt+"%"), "published" : ("=","1"),"start_date" : (">",now)}, order_by="start_date")

@frappe.whitelist(allow_guest=True)
def get_yellowpagesearch_result(txt):
	return frappe.get_all("Yellow Pages", fields=["*"], filters = {"business_name": ("like", "%"+txt+"%")})


@frappe.whitelist(allow_guest=True)
def get_yellowpagecategory_result(pageNo, size):
	category = frappe.get_all("Business Listing Category", fields=["*"],limit_start=pageNo,limit_page_length=size)
	if category:
		for i in category:
			subcategory = frappe.get_all("Business Listing Subcategories", fields=["*"],filters = {"category":i.name})
			if subcategory:
				i.subcount=len(subcategory)
			else: 
				Yellowpage = frappe.get_all("Yellow Pages", fields=["*"],filters = {"category":i.name})
				if subcategory:
					i.subcount=len(Yellowpage)
				else:	
					i.subcount=0
		return category

@frappe.whitelist(allow_guest=True)
def get_notification(name):	
 	Notification=frappe.db.sql('''select n.*,nl.status as view_status,nl.name as view_nme from `tabNotification` n left join `tabMember Notification List` nl on
 		n.name=nl.parent where nl.member=%(member)s order by creation desc limit {limit}'''.format(limit=30),{"member":name},as_dict=1)
 	return Notification

@frappe.whitelist(allow_guest=True)
def get_notification_count(name):	
 	Notification=frappe.db.sql('''select count(*) as notification_count from `tabNotification` n left join `tabMember Notification List` nl on
 		n.name=nl.parent where nl.member=%(member)s and nl.status="Not Visited" limit {limit}'''.format(limit=30),{"member":name},as_dict=1)
 	return Notification

@frappe.whitelist(allow_guest=True)
def get_advertisement(position,limit=1000):
 	ads=frappe.db.sql('''select p.*,si.ribbon_image,si.advertisement_count from `tabGSOD Promotions` p inner join `tabSponsorship` s on
 		p.sponsor=s.name inner join `tabSponsorship Items` si on si.name=s.sponsorship_plan
 		where p.position=%(position)s and p.status="Approved" and p.published=1 limit {limit}'''.format(limit=limit),{"position":position},as_dict=1)
 	return ads

@frappe.whitelist(allow_guest=True)
def update_task(member,task,status):
	task=frappe.db.get_all('Volunteer Task',fields=['name'],filters={'parent':task,'member':member})
	if task:
		for item in task:
			frappe.db.set_value('Volunteer Task',item.name,'completion_status',status)
		return 'Success' 

@frappe.whitelist(allow_guest=True)
def update_advertisement(name,views=None,status=None):
	advertisement=frappe.db.get_all('GSOD Promotions',fields=['name'],filters={'name':name})
	if views:
		if advertisement:
			for item in advertisement:
				frappe.db.set_value('GSOD Promotions',item.name,'views',views)
			return 'Success' 
	else:
	 	if advertisement:
			for item in advertisement:
				frappe.db.set_value('GSOD Promotions',item.name,'status',status)
			return 'Success' 

@frappe.whitelist(allow_guest=True)
def update_player_id(name,player_id):
	member=frappe.db.get_all('Member',fields=['name'],filters={'name':name})
	if member:
		for item in member:
			frappe.db.set_value('Member',item.name,'player_id',player_id)
		return 'Success' 

@frappe.whitelist(allow_guest=True)
def update_Expenseclaims(name,expense_receipt):
	expense=frappe.db.get_all('Expense Claims',fields=['name'],filters={'name':name})
	if expense:
		for item in expense:
			frappe.db.set_value('Expense Claims',item.name,'expense_receipt',expense_receipt)
		return 'Success' 

@frappe.whitelist(allow_guest=True)
def update_notification(name,status):
	notification=frappe.db.get_all('Member Notification List',fields=['name'],filters={'name':name})
	if notification:
		for item in notification:
			frappe.db.set_value('Member Notification List',item.name,'status',status)
		return 'Success' 

@frappe.whitelist(allow_guest=True)
def delete_volunteer(name,volunteer_skill):	
	frappe.db.sql('delete from `tabVolunteer Skill` where volunteer_skill=%(skill)s and parent=%(parent)s',{'skill':volunteer_skill,'parent':name})
	return 'Success'

@frappe.whitelist(allow_guest=True)
def volunteer_update(name,availability,availability_timeslot,volunteer_type,volunteer_skills):
	frappe.db.sql('''update `tabVolunteer` set availability=%(availability)s,availability_timeslot=%(availability_timeslot)s,volunteer_type=%(type)s where name=%(name)s''',
		{'availability':availability,'availability_timeslot':availability_timeslot,'name':name,'type':volunteer_type})
	data=json.loads(frappe.request.data)
	volunteerskills=data.get('volunteer_skills')
	if volunteerskills:	
		for item in volunteerskills:
			if not item.get('name'):
				frappe.get_doc({
					"doctype":"Volunteer Skill",
					"parent":name,
					"parenttype":"Volunteer",
					"parentfield":"volunteer_skills",
					"volunteer_skill":item.get('volunteer_skill')
					}).insert()
	return 'Success'