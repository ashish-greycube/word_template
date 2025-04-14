frappe.ui.form.on('Quotation',{
    refresh: function(frm) {
        frappe.db.get_doc('Word Template Settings', 'Word Template Settings')
            .then(doc => {
                console.log(doc, "======doc")
                if(doc.doctype_word_template.length > 0){
                    doc.doctype_word_template.forEach(temp => {
                        if(temp.doctype_name == frm.doc.doctype){
                            console.log(temp.template_name, "=====temp")
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
