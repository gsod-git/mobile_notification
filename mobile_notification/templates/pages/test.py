# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
from frappe.utils import (add_days, getdate, formatdate, get_first_day, date_diff,
                          add_years, get_timestamp, nowdate, flt, add_months, get_last_day)
import frappe


def get_context(context):

	tdate=frappe.utils.nowdate()
	exam = frappe.get_list("Exam", filters={"is_public": "Public", "start_date": ("<=", tdate), "end_date": (">=", tdate)},  
		fields=["test_name", "program", "course", "duration", "name", "multiple", "results_published", "publish_result", "start_date", "end_date"], 
		limit_page_length= 500)

	program = frappe.get_list("Program", fields=["program_name"], limit_page_length= 500)
	course = frappe.get_list("Course", fields=["course_name"], limit_page_length= 500)
	user = frappe.session.user
	result = frappe.get_list("Exam Result", fields=["user", "student", "exam_id"], filters={"user": user}, limit_page_length= 500)
	
	for i in exam:


		results = frappe.get_list("Exam Result", fields=["user", "student", "exam_id"], filters={"user": user, "exam_id": i.name}, limit_page_length= 500, )
		i.chapter = frappe.get_list("Exam Child", fields=["chapter", "question_type", "no_of_question"], filters={"parent": i.name}, limit_page_length= 500, )
		
		a = len(results)



		if a > 0:
		   count = 1
		   i.is_attended = 1
		   
		   if i.results_published == 1:
		   	i.show_result_now = 1
		   elif i.publish_result == "Publish Immediately":
		   	i.show_result_now = 1
		   else:	
		   	i.show_result_now = 0

		   if i.multiple == "One":
		   	i.show = 0
		   else:
		   	i.show = 1	

		else:
		   count = 0
		   i.show = 0
		   i.is_attended = 0

	context.tdate = tdate	   
	context.count = count
	context.course = course
	context.program = program
	context.exam = exam
	context.user = user
	context.result = result 
	context.results = results
    