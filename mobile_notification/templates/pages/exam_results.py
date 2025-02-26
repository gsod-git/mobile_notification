from __future__ import division
from __future__ import unicode_literals
import frappe


def get_context(context):

	user = frappe.session.user

	result = frappe.get_list("Exam Result", 
		fields=["user", "student", "exam_id", "exam_start_date", "exam_end_date", "name",
		"attended", "correct_answers", "wrong_answers", "total_marks", "secured__marks", "date_submitted"],
		filters={"user": user}, limit_page_length= 500, )
			 
	for x in result:
		x.answers = frappe.get_list("User Answer", 
		fields=["question_id", "question", "correct_answer", "user_answer", "is_user_answer_correct", "question_id"],
		filters={"parent": x.name, "parenttype": "Exam Result"}, limit_page_length= 500, )

		
		x.results_type = frappe.get_value("Exam", x.exam_id, "publish_result")

		if x.results_type == "Publish Immediately":
			x.results_published = 1
		
		if x.results_type == "Publish From Admin":
			x.results_published = frappe.get_value("Exam", x.exam_id, "results_published")


		x.program = frappe.get_value("Exam", x.exam_id, "program")
		x.course = frappe.get_value("Exam", x.exam_id, "course")

		x.exam_name = frappe.get_value("Exam", x.exam_id, "test_name")
		x.total_questions = len(x.answers)
		x.secured_per = int(x.secured__marks) / int(x.total_marks) * 100 
		x.secured_percentage = round(x.secured_per,2)
		


	context.result = result
	context.user = user


