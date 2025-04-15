import frappe
from frappe import _
from docx import Document
from docxtpl import DocxTemplate
from io import BytesIO

from frappe.utils import flt
from frappe.core.utils import html2text

@frappe.whitelist()
def create_and_download_docx_file(doctype: str, docname: str, word_template: str):
	data = frappe.get_doc(doctype, docname)
	data_dict = data.as_dict()

	for field in data.meta.fields:
		if field.fieldtype == "Date" and data.get(field.fieldname):
			data_dict[field.fieldname] = frappe.utils.get_datetime(data.get(field.fieldname)).strftime('%d-%m-%Y')
		if field.fieldtype == "Currency" and data.get(field.fieldname):
			money = flt(data.get(field.fieldname))
			data_dict[field.fieldname] = frappe.utils.fmt_money(money, currency=data.get("currency") )
		if (field.fieldtype == "Float" or field.fieldtype == "Int") and data.get(field.fieldname):
			data_dict[field.fieldname] = frappe.format(data.get(field.fieldname), {'fieldtype': 'Float'})
		if field.fieldtype == "Percent" and data.get(field.fieldname):
			data_dict[field.fieldname] = frappe.format(data.get(field.fieldname), {'fieldtype': 'Percent'})

		if field.fieldtype == "Table" and data.get(field.fieldname):
			data_dict[field.fieldname] = []

			for row in data.get(field.fieldname):
				row_dict = row.as_dict()

				for row_field in row.meta.fields:
					if row_field.fieldtype == "Date" and row.get(row_field.fieldname):
						row_dict[row_field.fieldname] = frappe.utils.get_datetime(row.get(row_field.fieldname)).strftime('%d-%m-%Y')
					if row_field.fieldtype == "Currency" and row.get(row_field.fieldname):
						money = flt(row.get(row_field.fieldname))
						row_dict[row_field.fieldname] = frappe.utils.fmt_money(money, currency=data.get("currency"))
					if (row_field.fieldtype == "Float" or row_field.fieldtype == "Int") and row.get(row_field.fieldname):
						row_dict[row_field.fieldname] = frappe.format(row.get(row_field.fieldname), {'fieldtype': 'Float'})
					if row_field.fieldtype == "Percent" and row.get(row_field.fieldname):
						row_dict[row_field.fieldname] = frappe.format(row.get(row_field.fieldname), {'fieldtype': 'Percent'})

				data_dict[field.fieldname].append(row_dict)

		if field.fieldtype == "Small Text" and data.get(field.fieldname):
			text_content = html2text(data.get(field.fieldname))
			data_dict[field.fieldname] = text_content
		
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
