// Copyright (c) 2024, hardik and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Brokerage Report"] = {
	"filters": [
		{
		"fieldname": "broker",
		"fieldtype": "Link",
		"label": "Sales Partner",
		"options": "Sales Partner",
		},
		{
		"fieldname": "from_date",
		"fieldtype": "Date",
		"label": "From Date",
		},
		{
		"fieldname": "to_date",
		"fieldtype": "Date",
		"label": "To Date",
		},
	],
	// onload: (report) => {
	// 	// Create a button for setting the default supplier
	// 	report.page.add_inner_button(__("Select Default Supplier"), () => {
	// 		let reporter = frappe.query_reports["Supplier Quotation Comparison"];

	// 		//Always make a new one so that the latest values get updated
	// 		reporter.make_default_supplier_dialog(report);
	// 	}, __("Tools"));

	// },
    // onload: (report) => {
    //     // Create a custom header with company name, address, and logo
    //     let custom_header = `
    //         <div id="custom-header" style="text-align: center; margin-bottom: 20px;">
    //             <img src="/path/to/your/logo.png" alt="Company Logo" style="height: 100px;">
    //             <h2>Company Name</h2>
    //             <p>Company Address Line 1</p>
    //             <p>Company Address Line 2</p>
    //         </div>
    //     `;

    //     // Append the custom header to the report's page
    //     $(report.page.main).prepend(custom_header);
    // }
};
