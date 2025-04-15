## Word Template

Generic App For Word Template

### Setup

1. In Word Template Settings Doctype

   In Word Template Child Table, Fill Word Template Details - Doctype Name, Attach Template, Template Name (Button Name)

2. For Each Doctype, Where word template download needed, Create Client Script

e.g, <br>
Doctype: Quotation <br>
Apply To : Form <br>

script:

```
frappe.ui.form.on('Quotation',{
    refresh: function(frm) {
        frappe.db.get_doc('Word Template Settings', 'Word Template Settings')
            .then(doc => {
                if(doc.doctype_word_template.length > 0){
                    doc.doctype_word_template.forEach(temp => {
                        if(temp.doctype_name == frm.doc.doctype){
                            frm.add_custom_button(__(temp.template_name), () => {
                                create_and_download_docx_file(frm, temp.word_template)
                            }, __("Download Word Template"))
                        }
                    });
                }
        })
    }
})

let create_and_download_docx_file = function(frm, word_template) {
    window.open(
        `/api/method/word_template.api.create_and_download_docx_file?doctype=${encodeURIComponent(
            frm.doc.doctype
        )}&docname=${encodeURIComponent(
            frm.doc.name
        )}&word_template=${encodeURIComponent(
            word_template
        )}`,
        "_blank"
    );
}

```

Note: To fetch doctype data write field name in curly brace e.g <b> {{name}} </b>

Ref: https://docxtpl.readthedocs.io/en/latest/

#### License

MIT
