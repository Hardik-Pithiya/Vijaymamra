# Copyright (c) 2024, hardik and contributors
# For license information, please see license.txt

import frappe
import os

def execute(filters=None):
    filters = filters or {}
    from_date = filters.get('from_date', '')
    to_date = filters.get('to_date', '')
    broker = filters.get('broker', '')
    
    columns = [
		{'label': '<b>Bill No</b>', 'fieldname': 'name', 'fieldtype': 'Link', 'options': 'Sales Invoice', 'width': 160},
        {'label': '<b>Customer Name</b>', 'fieldname': 'customer_name', 'fieldtype': 'Data', 'width': 160},
		{'label': '<b>Bill Date</b>', 'fieldname': 'posting_date', 'fieldtype': 'Data', 'width': 160},
		{'label': '<b>Broker Name</b>', 'fieldname': 'broker', 'fieldtype': 'Link', 'options': 'Sales Partner', 'width': 160},
		{'label': '<b>Item Name</b>', 'fieldname': 'item_name', 'fieldtype': 'Data', 'width': 160},
		{'label': '<b>Rate</b>', 'fieldname': 'rate', 'fieldtype': 'Data', 'width': 80},
		{'label': '<b>Quantity</b>', 'fieldname': 'qty', 'fieldtype': 'Data', 'width': 80},
		{'label': '<b>Brockrage Rate</b>', 'fieldname': 'rate_with_type', 'fieldtype': 'Data', 'width': 160},
		{'label': '<b>Total</b>', 'fieldname': 'total', 'fieldtype': 'Data', 'width': 80},
	]

    sql = """
    	SELECT 
            SI.name,
            SI.customer_name,
            SI.posting_date,
            SP.name as broker,
            SII.item_name,
            SII.rate,
            SII.qty,
    		COALESCE(CONCAT(ROUND(SPR.rate, 2), ' ', SPR.type), ' - ') AS rate_with_type,
            COALESCE(
                CASE 
                    WHEN SPR.type = 'KG' THEN SPR.rate * SII.total_weight
                    WHEN SPR.type = 'Nos' THEN SPR.rate * SII.qty
                    WHEN SPR.type = 'Amount' THEN SPR.rate * SII.amount
                END, 0) AS total
		FROM
			`tabSales Invoice` AS SI
		JOIN `tabSales Invoice Item` AS SII ON SI.name = SII.parent AND SI.docstatus = 1
		LEFT JOIN `tabSales Partner` AS SP ON SP.name = SI.sales_partner
		LEFT JOIN `tabSales Partner Rate` AS SPR ON SP.name = SPR.parent AND SPR.item_code = SII.item_code
		WHERE
            (SI.posting_date BETWEEN %s AND %s OR %s = '' OR %s = '')
            AND (SP.name = %s OR %s = '')
        ORDER BY 
            SI.posting_date DESC
    """
    filters = (from_date, to_date, from_date, to_date, broker, broker)

    data = frappe.db.sql(sql, filters, as_dict=True)

    # # Read the custom header HTML file content
    # header_path = os.path.join(frappe.get_app_path('vijaymamra'), 'public', 'html', 'custom_header.html')
    # with open(header_path, 'r') as file:
    #     custom_header = file.read()

    # company_name = frappe.defaults.get_user_default("Company")

    # company = frappe.get_doc("Company", company_name)
    # company_logo = company.company_logo

    # custom_header = custom_header.replace("{{ company_name }}", company_name)
    # # custom_header = custom_header.replace("{{ company_address }}", company_address)
    # custom_header = custom_header.replace("{{ company_logo }}", company_logo)

    return columns, data#, custom_header

    # message = '<div style="text-align: center; margin-bottom: 20px;"><img src="/path/to/your/logo.png" alt="Company Logo" style="height: 100px;"><h2>Company Name</h2><p>Company Address Line 1</p><p>Company Address Line 2</p></div>'
    # return columns, data, message

