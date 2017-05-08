from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Purchasing"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Supplier Quotation",
					"description": _("Quotations received from Suppliers."),
				},
				{
					"type": "doctype",
					"name": "Purchase Order",
					"description": _("Purchase Orders given to Suppliers."),
				},
				{
					"type": "doctype",
					"name": "Payment Entry",
					"description": _("Bank/Cash transactions against party or for internal transfer")
				},
            ]
		},
		{
			"label": _("Supplier"),
			"items": [
				{
					"type": "doctype",
					"name": "Supplier",
					"description": _("Supplier database."),
				},
				{
					"type": "doctype",
					"name": "Supplier Type",
					"description": _("Supplier Type master.")
				},
				{
					"type": "doctype",
					"name": "Contact",
					"description": _("All Contacts."),
				},
				{
					"type": "doctype",
					"name": "Address",
					"description": _("All Addresses."),
				},

			]
		},
		{
			"label": _("Setup"),
			"icon": "icon-cog",
			"items": [
				{
					"type": "doctype",
					"name": "Buying Settings",
					"description": _("Default settings for buying transactions.")
				},
				{
					"type": "doctype",
					"name":"Terms and Conditions",
					"label": _("Terms and Conditions Template"),
					"description": _("Template of terms or contract.")
				},
				{
					"type": "doctype",
					"name": "Purchase Taxes and Charges Template",
					"description": _("Tax template for buying transactions.")
				},
			]
		},
		{
			"label": _("Items and Pricing"),
			"items": [
				{
					"type": "doctype",
					"name": "Item",
					"description": _("All Products or Services."),
				},
				{
					"type": "doctype",
					"name": "Price List",
					"description": _("Price List master.")
				},
				{
					"type": "doctype",
					"name": "Item Price",
					"description": _("Multiple Item prices."),
					"route": "Report/Item Price"
				},
			]
		},
		{
			"label": _("Reports"),
			"icon": "icon-table",
			"items": [
				{
					"type": "page",
					"name": "purchase-analytics",
					"label": _("Purchase Analytics"),
					"icon": "icon-bar-chart",
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Supplier-Wise Sales Analytics",
					"doctype": "Stock Ledger Entry"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Purchase Order Trends",
					"doctype": "Purchase Order"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Item-wise Purchase History",
					"doctype": "Item"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Supplier Addresses and Contacts",
					"doctype": "Supplier"
				},
			]
		},
	]
