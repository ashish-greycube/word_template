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
        if (frm.is_dirty()==true) {
            frappe.throw({
                message: __("Please save the form to proceed..."),
                indicator: "red",
            });       
        }
        return frappe.call({
            method: "word_template.api.create_and_download_docx_file",
            args: {
                doctype: frm.doc.doctype,
                docname:frm.doc.name,
                word_template: word_template,
            },
            callback: function (r) {
                console.log(r.message)
                let file_path = r.message[0]
                let file_name = r.message[1]
                function downloadURI(uri, name) 
                {
                    var link = document.createElement("a");
                    // If you don't know the name or want to use
                    // the webserver default set name = ''
                    link.setAttribute('download', name);
                    link.href = uri;
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                }                    
                downloadURI(file_path,file_name)
                frappe.call({
                    method: "word_template.api.delete_file",
                    args: {
                        file_name:file_name
                    },
                    callback: function (r) {
                    console.log(r.message)
                    }
                })
                }
            })

    // window.open(
    //     `/api/method/word_template.api.create_and_download_docx_file?doctype=${encodeURIComponent(
    //         frm.doc.doctype
    //     )}&docname=${encodeURIComponent(
    //         frm.doc.name
    //     )}&word_template=${encodeURIComponent(
    //         word_template
    //     )}`,
    //     "_blank"
    // ) 
}
