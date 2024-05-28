frappe.ui.form.on('Payment Entry', {
    before_cancel: function(frm) {
        frappe.call({
            method: 'vijaymamra.public.py.payment_entry.check_entries',
            args: {
                payment_entry_name: frm.doc.name
            },
            callback: function(response) {
                console.log(response)
                if (response.message.matched) {
                    frappe.msgprint(__('This Payment Entry is linked with a reconciled Bank Transaction and cannot be canceled.'));
                    frappe.validated = false;
                } else {
                    frm.savesubmit(); 
                }
            }
        });
    }
});
// apps/vijaymamra/vijaymamra/public/py/payment_entry.py