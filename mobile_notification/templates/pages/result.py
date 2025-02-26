from __future__ import division
from __future__ import unicode_literals
import frappe


def get_context(context):

	user = frappe.session.user
	ExamId = frappe.form_dict.Exam

	result = frappe.get_list("Exam Result", fields=["user", "student", "exam_id", "exam_start_date", "exam_end_date", "name",
													"attended", "correct_answers", "wrong_answers", "total_marks", "secured__marks"],
													filters={"user": user, "exam_id": ExamId}, limit_page_length= 500, )
	for x in result:
		x.answers = frappe.get_list("User Answer", fields=["question_id", "question", "correct_answer", "user_answer", "is_user_answer_correct", "question_id"],
												   filters={"parent": x.name, "parenttype": "Exam Result"}, limit_page_length= 500, )
		
		x.exam_type = frappe.get_value("Exam", ExamId, "is_public")
		x.scholarship = frappe.get_value("Exam", ExamId, "scholarship")
		x.secured_per = int(x.secured__marks) / int(x.total_marks) * 100 
		x.secured_percentage = round(x.secured_per,2)
		x.exam_name = frappe.get_value("Exam", ExamId, "test_name")
		x.sch_details = frappe.get_all("Mark Range", fields=["from_mark", "to_mark", "scholarship"],
		filters=[["parent", "=", x.scholarship], ["from_mark", "<=", x.secured_percentage], ["to_mark", ">=", x.secured_percentage]])
		x.discount_per = x.sch_details[0].scholarship
		x.answers_len = len(x.answers)

		for y in x.answers:
			y.options = frappe.get_list("Answers", fields=["options", "is_correct"],
													   filters={"parent": y.question_id}, limit_page_length= 500, )
		

	context.result = result
	context.user = user
	context.exam_id = ExamId
