// Copyright (c) 2023, hardik and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gate Pass', {
		on_submit:function(frm) {
	    frappe.call({
	        method:'vijaymamra.vijaymamra.doctype.gate_pass.gate_pass.update_status',
	        args:{
	            data :frm.doc.items,
	            name :frm.doc.name,
	        }
	    })
	}
});
