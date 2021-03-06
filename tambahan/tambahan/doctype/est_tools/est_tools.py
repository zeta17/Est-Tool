# -*- coding: utf-8 -*-
# Copyright (c) 2015, hendrik and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from dateutil import parser
from frappe.model.mapper import get_mapped_doc

class EstTools(Document):
	def autoname(self):
		ym = parser.parse(self.posting_date).strftime('%y%m')
		self.name = make_autoname("EST-"+ym+".###")
		
	#def validate(self):
		#pass
		#frappe.throw(_("Anda pilih: "+self.item_name))
	def get_details(self):
		dl = frappe.db.sql("""select b1.item_code, b1.item_name, b1.qty, b1.stock_uom, b1.rate, b1.amount
			from
				`tabBOM Item` b1
			where
				b1.parent = %s
			order by b1.idx ASC""", self.bill_of_material, as_dict=1)
		
		self.set('item_utama', [])
		
		for d in dl:
			nl = self.append('item_utama', {})
			nl.item_code = d.item_code
			nl.item_name = d.item_name
			nl.quantity = d.qty
			nl.uom = d.stock_uom
			nl.price_list_rate = d.rate
			nl.rate = d.rate
			nl.amount = d.amount
			nl.net_amount = d.amount
			nl.factor_1 = "1"
			nl.factor_2 = "1"
			nl.factor_3 = "1"
			nl.factor_4 = "1"
			nl.factor_5 = "1"
			
	def make_bom(self):
		frappe.msgprint("Hai, Behind you")
	
			
@frappe.whitelist()
def test_method(source_name, target_doc=None):
	doc = get_mapped_doc("Est Tools", source_name, {
		"Est Tools": {
			"doctype": "BOM",
			"field_map": {
				"item_code": "item"
			},
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Est Tools Primary Item": {
			"doctype": "BOM Item",
			"field_map": {
				"quantity": "qty",
				"uom": "stock_uom",
				"net_amount": "amount"
			}
		},
		"Est Tools Secondary Item": {
			"doctype": "BOM Item",
			"field_map": {
				"si_qty": "qty",
				"uom": "stock_uom",
				"si_rate":"rate",
				"si_net_amount": "amount"
			}
		},
	}, target_doc)
	
	return doc