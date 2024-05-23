// Copyright (c) 2024, hardik and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Purchase Brokerage Report"] = {
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
	]
};
