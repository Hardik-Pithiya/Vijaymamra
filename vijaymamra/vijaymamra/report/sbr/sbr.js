// Copyright (c) 2024, hardik and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["sbr"] = {
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
