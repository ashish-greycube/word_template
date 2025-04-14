import frappe
from frappe import _
from docx import Document
from docxtpl import DocxTemplate
from io import BytesIO

from frappe.utils import flt

@frappe.whitelist()
def create_and_download_docx_file(doctype: str, docname: str, word_template: str):
	data = frappe.get_doc(doctype, docname)

	for field in data.meta.fields:
		if field.fieldtype == "Date" and data.get(field.fieldname):
			data.set(field.fieldname, frappe.utils.get_datetime(data.get(field.fieldname)).strftime('%d-%m-%Y'))
		if field.fieldtype == "Currency" and data.get(field.fieldname):
			money = flt(data.get(field.fieldname))
			data.set(field.fieldname,  frappe.utils.fmt_money(money, currency=data.get("currency") ))
			data.set(field.fieldname + "_formatted", frappe.utils.fmt_money(money, currency=data.get("currency")))
		
			print(field.fieldname, "----",data.get(field.fieldname), "====", frappe.utils.fmt_money(money, currency=data.get("currency")))

		print(data.get('total_formatted'), "======_formatted")

	# data.transaction_date = frappe.utils.get_datetime(data.transaction_date).strftime('%d %b %Y')
	# data["pageBreak"] = "\f"

	data_dict = data.as_dict()
	
	template_doc = frappe.get_doc("File", {"file_url":word_template})
	template_path = template_doc.get_full_path()
	output_file = _fill_template(template_path, data_dict)
	file_name = "-".join([docname, template_doc.file_name])

	frappe.local.response.filename = file_name
	frappe.local.response.filecontent = output_file.getvalue()
	frappe.local.response.type = "download"

def _fill_template(template, data):
	doc = DocxTemplate(template)
	# pi_doc = frappe.get_doc(data.doctype, data.name)
	# records = pi_doc.items
	# data.posting_date = frappe.utils.get_datetime(data.posting_date).strftime('%d %b %Y') 
	# data["records"] = records
	# data["pageBreak"] = "\f"

	doc.render(data)
	_file = BytesIO()
	doc.docx.save(_file)
	return _file
