# Copyright (c) 2024, hardik and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns, data = get_columns(), get_data()
    return columns, data


def get_columns():
    return [
        _("Invoice Name") + ":Link/Sales Invoice:150",
        _("Gate Pass Out Name") + ":Data:150",
        _("Invoice Posting Date") + ":Date:150",
        _("Gate Pass Out Date") + ":Date:150",
        _("Vehicle Number") + ":Data:150",
        _("Net Weight") + ":Float:150",
        _("Tolerance") + ":Float:150",
        _("Check Gate Pass") + ":Int:150",
    ]


def get_data():
    query = """
        SELECT
            si.name AS `invoice_name`,
            gpo.name AS `gate_pass_out_name`,
            si.posting_date AS `invoice_posting_date`,
            gpo.posting_date AS `gate_pass_out_date`,
            gpo.vehicle_number,
            gpo.net_weight,
            gpo.tolerance_in_ AS `tolerance`,
            si.custom_gate_pass_out AS `check_gate_pass`
        FROM
            `tabSales Invoice` AS si
        LEFT JOIN
            `tabInvoice Details` AS id ON si.name = id.invoice_number
        LEFT JOIN
            `tabGate Pass Out` AS gpo ON id.parent = gpo.name
    """
    data = frappe.db.sql(query, as_dict=True)
    return data
