frappe.ui.form.on("Sales Invoice", {
    validate: function(frm) {
        if (frm.doc.custom_transaction_type_ === "GST Tax Invoice") {
            // Array to hold all promises
            let promises = frm.doc.items.map(function(row) {
                return frappe.call({
                    method: "frappe.client.get_value",
                    args: {
                        doctype: "Item",
                        filters: {
                            item_code: row.item_code
                        },
                        fieldname: "is_nil_exempt"
                    }
                }).then(r => {
                    if (r.message && r.message.is_nil_exempt == 1) {
                        frappe.throw("Item " + row.item_code + " (" + row.item_name + ") is marked as 'Nil Exempt', which is not allowed for GST Tax Invoice.");
                    }
                });
            });
            // Use Promise.all to wait for all promises to resolve
            return Promise.all(promises);
        } else {
            // Array to hold all promises
            let promises = frm.doc.items.map(function(row) {
                return frappe.call({
                    method: "frappe.client.get_value",
                    args: {
                        doctype: "Item",
                        filters: {
                            item_code: row.item_code
                        },
                        fieldname: "is_nil_exempt"
                    }
                }).then(r => {
                    if (r.message && r.message.is_nil_exempt == 0) {
                        frappe.throw("Item " + row.item_code + " (" + row.item_name + ") is not marked as 'Nil Exempt', which is required for Bill of Supply.");
                    }
                });
            });
            // Use Promise.all to wait for all promises to resolve
            return Promise.all(promises);
        }
    }
});