# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
import frappe.defaults
from frappe import _, msgprint
from frappe.contacts.address_and_contact import (
	delete_contact_and_address,
	load_address_and_contact,
)
from frappe.model.naming import set_name_by_naming_series, set_name_from_naming_options

from erpnext.accounts.party import (  # noqa
	get_dashboard_info,
	validate_party_accounts,
)
from erpnext.utilities.transaction_base import TransactionBase



class Supplier(TransactionBase):
	def get_feed(self):
		return self.supplier_name

	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)
		self.load_dashboard_info()

	def before_save(self):
		if not self.on_hold:
			self.hold_type = ""
			self.release_date = ""
		elif self.on_hold and not self.hold_type:
			self.hold_type = "All"

	def load_dashboard_info(self):
		info = get_dashboard_info(self.doctype, self.name)
		self.set_onload("dashboard_info", info)

	def autoname(self):
		supp_master_name = frappe.defaults.get_global_default("supp_master_name")
		if supp_master_name == "Supplier Name":
			if self.supplier_group == "Brokers":
				value = "BR.#####"	
				
				self.naming_series = value
				self.custom_series = value

			elif self.supplier_group == "Machine Hardware and Electrical":
				value = "MH.#####"	
				
				self.naming_series = value
				self.custom_series = value			
			elif self.supplier_group == "Makkai Poha":
				value = "CF.#####"

				self.naming_series = value
				self.custom_series = value
			elif self.supplier_group == "Poha Supplier":
				value = "POS.#####"

				self.naming_series = value
				self.custom_series = value

			elif self.supplier_group == "Transport":
				value = "TR.#####"

				self.naming_series = value
				self.custom_series = value

			elif self.supplier_group == "Labour":
				value = "LR.#####"

				self.naming_series = value
				self.custom_series = value			

			else:
				lists = self.supplier_group
				lists1 = lists.split(" ")
				series = ""
				
				for word in lists1:
					series += word[0]
				
				value = series + ".#####" 
				self.custom_series = value
				self.naming_series = value
				
			set_name_by_naming_series(self)    	
						
		elif supp_master_name == "Naming Series":			
			self.name = self.supplier_name
		else:
			self.name = set_name_from_naming_options(frappe.get_meta(self.doctype).autoname, self)

	def on_update(self):
		if not self.naming_series:
			self.naming_series = ""

		self.create_primary_contact()
		self.create_primary_address()

	def validate(self):
		self.flags.is_new_doc = self.is_new()

		# validation for Naming Series mandatory field...
		if frappe.defaults.get_global_default("supp_master_name") == "Naming Series":
			if not self.naming_series:
				msgprint(_("Series is mandatory"), raise_exception=1)

		validate_party_accounts(self)
		self.validate_internal_supplier()

	@frappe.whitelist()
	def get_supplier_group_details(self):
		doc = frappe.get_doc("Supplier Group", self.supplier_group)
		self.payment_terms = ""
		self.accounts = []

		if doc.accounts:
			for account in doc.accounts:
				child = self.append("accounts")
				child.company = account.company
				child.account = account.account

		if doc.payment_terms:
			self.payment_terms = doc.payment_terms

		self.save()

	def validate_internal_supplier(self):
		if not self.is_internal_supplier:
			self.represents_company = ""

		internal_supplier = frappe.db.get_value(
			"Supplier",
			{
				"is_internal_supplier": 1,
				"represents_company": self.represents_company,
				"name": ("!=", self.name),
			},
			"name",
		)

		if internal_supplier:
			frappe.throw(
				_("Internal Supplier for company {0} already exists").format(
					frappe.bold(self.represents_company)
				)
			)

	def create_primary_contact(self):
		from erpnext.selling.doctype.customer.customer import make_contact

		if not self.supplier_primary_contact:
			if self.mobile_no or self.email_id:
				contact = make_contact(self)
				self.db_set("supplier_primary_contact", contact.name)
				self.db_set("mobile_no", self.mobile_no)
				self.db_set("email_id", self.email_id)

	def create_primary_address(self):
		from frappe.contacts.doctype.address.address import get_address_display

		from erpnext.selling.doctype.customer.customer import make_address

		if self.flags.is_new_doc and self.get("address_line1"):
			address = make_address(self)
			address_display = get_address_display(address.name)

			self.db_set("supplier_primary_address", address.name)
			self.db_set("primary_address", address_display)

	def on_trash(self):
		if self.supplier_primary_contact:
			self.db_set("supplier_primary_contact", None)
		if self.supplier_primary_address:
			self.db_set("supplier_primary_address", None)

		delete_contact_and_address("Supplier", self.name)

	def after_rename(self, olddn, newdn, merge=False):
		if frappe.defaults.get_global_default("supp_master_name") == "Supplier Name":
			self.db_set("supplier_name", newdn)


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_supplier_primary_contact(doctype, txt, searchfield, start, page_len, filters):
	supplier = filters.get("supplier")
	return frappe.db.sql(
		"""
		SELECT
			`tabContact`.name from `tabContact`,
			`tabDynamic Link`
		WHERE
			`tabContact`.name = `tabDynamic Link`.parent
			and `tabDynamic Link`.link_name = %(supplier)s
			and `tabDynamic Link`.link_doctype = 'Supplier'
			and `tabContact`.name like %(txt)s
		""",
		{"supplier": supplier, "txt": "%%%s%%" % txt},
	)





@frappe.whitelist()
def check_entries(payment_entry_name=None):
    payment_entries = frappe.get_all("Payment Entry", filters={"status": "Submitted"}, fields=["name"])
    
    bank_transactions = frappe.get_all("Bank Transaction", filters={"status": "reconciled"}, fields=["name"])

    matched_entries = []

    for bank_transaction in bank_transactions:
        bank_transaction_doc = frappe.get_doc("Bank Transaction", bank_transaction['name'])
        for payment in bank_transaction_doc.payment_entries:
            for payment_entry in payment_entries:
                if payment.payment_entry == payment_entry['name']:
                    matched_entries.append(payment_entry['name'])

    if payment_entry_name and payment_entry_name in matched_entries:
        return {"matched": True, "entries": matched_entries}
    return {"matched": False, "entries": matched_entries}