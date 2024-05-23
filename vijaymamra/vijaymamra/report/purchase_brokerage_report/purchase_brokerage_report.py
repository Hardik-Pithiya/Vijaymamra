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
		{'label': '<b>Bill No</b>', 'fieldname': 'name', 'fieldtype': 'Link', 'options': 'Purchase Invoice', 'width': 160},
        {'label': '<b>Supplier Name</b>', 'fieldname': 'supplier_name', 'fieldtype': 'Data', 'width': 160},
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
            PI.name,
            PI.supplier_name,
            PI.posting_date,
            SP.name as broker,
            PII.item_name,
            PII.rate,
            PII.qty,
    		COALESCE(CONCAT(ROUND(SPR.rate, 2), ' ', SPR.type), ' - ') AS rate_with_type,
            COALESCE(
                CASE 
                    WHEN SPR.type = 'KG' THEN SPR.rate * PII.total_weight
                    WHEN SPR.type = 'Nos' THEN SPR.rate * PII.qty
                    WHEN SPR.type = 'Amount' THEN SPR.rate * PII.amount
                END, 0) AS total
		FROM
			`tabPurchase Invoice` AS PI
		JOIN `tabPurchase Invoice Item` AS PII ON PI.name = PII.parent AND PI.docstatus = 1
		LEFT JOIN `tabSales Partner` AS SP ON SP.name = PI.custom_broker
		LEFT JOIN `tabSales Partner Rate` AS SPR ON SP.name = SPR.parent AND SPR.item_code = PII.item_code
		WHERE
            (PI.posting_date BETWEEN %s AND %s OR %s = '' OR %s = '')
            AND (SP.name = %s OR %s = '')
        ORDER BY 
            PI.posting_date DESC
    """
    filters = (from_date, to_date, from_date, to_date, broker, broker)
    data = frappe.db.sql(sql, filters, as_dict=True)
    return columns, data