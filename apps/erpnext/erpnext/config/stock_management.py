from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Inventory"),
			"items": [
				{
					"type": "doctype",
					"name": "Item",
					"description": _("All Products."),
                    "label": _("Items / Products List"),
				},
				{
					"type": "doctype",
					"name": "Item Attribute",
					"description": _("Attributes for Item Variants. e.g Size, Color etc."),
                    "label": _("Item Variants"),
				},
				{
					"type": "doctype",
					"name": "Brand",
					"description": _("Brand master."),
                    "label": _("Product Brands"),
				},
				{
					"type": "doctype",
					"name": "Stock Entry",
                    "label": _("Material Transfer"),
                    "link": "Form/Stock Entry/New Stock Entry/Material Transfer",
					"description": _("Record item movement."),
				},
				{
					"type": "doctype",
					"name": "Stock Entry",
                    "label": _("Material Issue"),
                    "link": "Form/Stock Entry/New Stock Entry/Material Issue",
					"description": _("Record item movement."),
				},
				{
					"type": "doctype",
					"name": "Stock Entry",
                    "label": _("Material Receipt"),
                    "link": "Form/Stock Entry/New Stock Entry/Material Receipt",
					"description": _("Record item movement."),
				},
			]
		},
		{
			"label": _("Warehouse"),
			"icon": "icon-cog",
			"items": [
				{
					"type": "doctype",
					"name": "Warehouse",
					"description": _("Where items are stored."),
                    "label": _("Stores / Warehouses"),
				},
				{
					"type": "doctype",
					"name": "Purchase Receipt",
					"description": _("Goods received from Suppliers."),
				},
			]
		},
		{
			"label": _("Tools"),
			"icon": "icon-wrench",
			"items": [
				{
					"type": "doctype",
					"name": "Stock Reconciliation",
					"description": _("Upload stock balance via csv.")
				},
				{
					"type": "doctype",
					"name": "Packing Slip",
					"description": _("Split Delivery Note into packages.")
				},
			]
		},
		{
			"label": _("Reports"),
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Stock Ledger",
					"doctype": "Stock Ledger Entry",
                    "label": _("Stock Flow"),
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Stock Balance",
					"doctype": "Stock Ledger Entry",
                    "label": _("Stock Card"),
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Stock Projected Qty",
					"doctype": "Item",
                    "label": _("Stock Position"),
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Stock Ageing",
					"doctype": "Item",
				},
				{
					"type": "report",
					"name": "Item Shortage Report",
					"route": "Report/Bin/Item Shortage Report",
					"doctype": "Purchase Receipt",
				},

			]
		},
	]
