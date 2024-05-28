import frappe


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