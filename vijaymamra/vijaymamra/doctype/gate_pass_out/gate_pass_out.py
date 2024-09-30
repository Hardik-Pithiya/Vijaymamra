# Copyright (c) 2023, hardik and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class GatePassOut(Document):
    def on_submit(self):
        si_data = self.invoice_details
        
        for item in si_data:
            if item.invoice_number:
                frappe.db.set_value("Sales Invoice", item.invoice_number, "custom_gate_pass_out", 1)
            if item.purchase_receipt:
                frappe.db.set_value("Purchase Receipt", item.purchase_receipt, "custom_gate_pass_out", 1)
    def before_cancel(self):
        si_data = self.invoice_details
        for item in si_data:
            if item.invoice_number:
                frappe.db.set_value("Sales Invoice", item.invoice_number, "custom_gate_pass_out", 0)
            if item.purchase_receipt:
                frappe.db.set_value("Purchase Receipt", item.purchase_receipt, "custom_gate_pass_out", 0)
        