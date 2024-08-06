# Copyright (c) 2023, hardik and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class GatePassOut(Document):
	def on_submit(self):
		si_data = self.invoice_details

		for item in si_data:
			frappe.db.set_value("Sales Invoice", item.get('invoice_number'), "custom_gate_pass_out", 1)