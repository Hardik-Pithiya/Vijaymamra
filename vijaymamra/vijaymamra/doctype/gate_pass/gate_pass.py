# Copyright (c) 2023, hardik and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class GatePass(Document):
	pass

@frappe.whitelist()
def update_status(data, name):
	data1 = json.loads(data)

	all_good_received = all(item.get('status') == 'Good Received' for item in data1)

	if all_good_received:
		frappe.db.set_value("Gate Pass", name, "docstatus", 3)
