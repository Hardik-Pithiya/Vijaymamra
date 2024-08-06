// Copyright (c) 2023, hardik and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gate Pass Out', {
	onload: function (frm) {
		frm.set_query('invoice_number', 'invoice_details', function (doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: {
					'custom_gate_pass_out': 0,
					'docstatus':1
				}
			};
		});
	}

});

