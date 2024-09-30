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

		frm.set_query('purchase_receipt', 'invoice_details', function (doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: {
					'custom_gate_pass_out': 0,
					'docstatus':1
				}
			};
		});

	},
	refresh: function (frm) {
        // Call check_wards on form refresh
       frm.doc.invoice_details.forEach(function(row, index) {
            check_wards(frm, 'Invoice Details', row.name);
        });
    }

});


frappe.ui.form.on('Invoice Details', {
	refresh:function(frm,cdt,cdn){
		check_wards(frm,cdt,cdn)
	},
	wards:function(frm,cdt,cdn){
		check_wards(frm,cdt,cdn)
		
	}
})






function check_wards(frm, cdt, cdn) {
    var data = locals[cdt][cdn]; // Get the current row

    // Check if the child table has rows
    if (frm.doc.invoice_details && frm.doc.invoice_details.length > 0) {
        // Loop through all rows in the grid
        frm.doc.invoice_details.forEach(function (row, index) {
            // Check the value of 'wards' in each row and set properties accordingly
            if (row.wards === "In Wards") {
                
				// // Show fields
				frm.set_df_property('invoice_details', 'read_only', 1, frm.doc.name, 'invoice_number', row.name)
				frm.set_df_property('invoice_details', 'read_only', 0, frm.doc.name, 'purchase_receipt', row.name)

				frm.set_df_property('invoice_details', 'read_only', 0, frm.doc.name, 'supplier', row.name)
				frm.set_df_property('invoice_details', 'read_only', 0, frm.doc.name, 'supplier_name', row.name)
				frm.set_df_property('invoice_details', 'read_only', 0, frm.doc.name, 'pr_weight', row.name)
				frm.set_df_property('invoice_details', 'read_only', 0, frm.doc.name, 'pr_qty', row.name)
				frm.set_df_property('invoice_details', 'read_only', 0, frm.doc.name, 'pr_bag', row.name)
				
                // Set read-only and hidden properties for the respective fields in the child table
                frm.fields_dict['invoice_details'].grid.grid_rows[index].toggle_editable('invoice_number', false);
                frm.fields_dict['invoice_details'].grid.grid_rows[index].toggle_editable('purchase_receipt', true);

                // Clear fields
                row.invoice_number = "";
                row.customer_code = "";
                row.customer_name = "";
                row.total_quantity = "";
                row.total_bag = "";
            }
			if (row.wards === "Out Wards") {

				

				frm.set_df_property('invoice_details', 'read_only', 0, frm.doc.name, 'invoice_number', row.name)
				frm.set_df_property('invoice_details', 'read_only', 1, frm.doc.name, 'purchase_receipt', row.name)
				frm.set_df_property('invoice_details', 'read_only', 1, frm.doc.name, 'supplier', row.name)
				frm.set_df_property('invoice_details', 'read_only', 1, frm.doc.name, 'supplier_name', row.name)
				frm.set_df_property('invoice_details', 'read_only', 1, frm.doc.name, 'pr_weight', row.name)
				frm.set_df_property('invoice_details', 'read_only', 1, frm.doc.name, 'pr_qty', row.name)
				frm.set_df_property('invoice_details', 'read_only', 1, frm.doc.name, 'pr_bag', row.name)

				
                // Set blank value
                frm.fields_dict['invoice_details'].grid.grid_rows[index].toggle_editable('invoice_number', true);
                frm.fields_dict['invoice_details'].grid.grid_rows[index].toggle_editable('purchase_receipt', false);

              
                // Clear fields
                row.purchase_receipt = "";
                row.supplier = "";
                row.supplier_name = "";
                row.pr_qty = "";
                row.pr_bag = "";
            }
        });
		// Refresh the child table to apply changes
		frm.refresh_field('invoice_details');
    }

    
}


