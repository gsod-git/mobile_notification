from __future__ import division
from __future__ import unicode_literals
import frappe


def get_context(context):

	user = frappe.session.user

	result = frappe.get_list("Exam Result", fields=["user", "student", "exam_id", "exam_start_date", "exam_end_date", "name",
													"attended", "correct_answers", "wrong_answers", "total_marks", "secured__marks"],
													filters={"user": user}, limit_page_length= 500, )


	context.result = result
	context.user = user
