# Copyright (c) 2024, hardik and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    filters = filters or {}
    from_date = filters.get('from_date', '')
    to_date = filters.get('to_date', '')
    broker = filters.get('broker', '')
    
    columns = [
		{'label': '<b>Bill No</b>', 'fieldname': 'name', 'fieldtype': 'Data', 'width': 150},
		{'label': '<b>Bill Date</b>', 'fieldname': 'posting_date', 'fieldtype': 'Data', 'width': 150},
		{'label': '<b>Name</b>', 'fieldname': 'broker', 'fieldtype': 'Data', 'width': 150},
		{'label': '<b>Item Name</b>', 'fieldname': 'item_name', 'fieldtype': 'Data', 'width': 150},
		{'label': '<b>Rate</b>', 'fieldname': 'rate', 'fieldtype': 'Data', 'width': 150},
		{'label': '<b>Quantity</b>', 'fieldname': 'qty', 'fieldtype': 'Data', 'width': 150},
		{'label': '<b>Brockrage Rate</b>', 'fieldname': 'rate_with_type', 'fieldtype': 'Data', 'width': 150},
		{'label': '<b>Total</b>', 'fieldname': 'total', 'fieldtype': 'Data', 'width': 150}
	]

    sql = """
    	SELECT 
            SI.name,
            SI.posting_date,
            SP.name as broker,
            SII.item_name,
            SII.rate,
            SII.qty,
    		CONCAT(ROUND(SPR.rate, 2), ' ', SPR.type) AS rate_with_type,
        CASE 
            WHEN SPR.type = 'KG' THEN SPR.rate * SII.total_weight
            WHEN SPR.type = 'Nos' THEN SPR.rate * SII.qty
            WHEN SPR.type = 'Amount' THEN SPR.rate * SII.amount
        END AS total
		FROM
			`tabSales Invoice` AS SI
		JOIN `tabSales Invoice Item` AS SII ON SI.name = SII.parent AND SI.docstatus = 1
		JOIN `tabSales Partner` AS SP ON SP.name = SI.sales_partner
		JOIN `tabSales Partner Rate` AS SPR ON SP.name = SPR.parent AND SPR.item_code = SII.item_code
		WHERE
            (SI.posting_date BETWEEN %s AND %s OR %s = '' OR %s = '')
            AND (SP.name = %s OR %s = '')
        ORDER BY 
            SI.name
    """
    filters = (from_date, to_date, from_date, to_date, broker, broker)

    data = frappe.db.sql(sql, filters, as_dict=True)
    return columns, data

