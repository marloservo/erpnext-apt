from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Sales"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Sales Invoice",
					"description": _("Confirmed orders from Customers."),
				},
				{
					"type": "doctype",
					"name": "Customer",
					"description": _("Customer database."),
				},
				{
					"type": "doctype",
					"name": "Item",
					"description": _("All Products."),
                    "label": _("Items / Products List"),
				},
			]
		},
		{
			"label": _("Upload Data"),
            "icon": "icon-upload-alt",
			"items": [
				{
					"type": "page",
					"name": "import-sales-report",
					"label": _("Upload Sales Report"),
					"icon": "icon-upload-alt",
				},                
            ]
        },
		{
			"label": _("Setup"),
			"items": [
				{
					"type": "doctype",
					"name": "Price List",
					"description": _("Price List master."),
				},
				{
					"type": "doctype",
					"name": "Customer Group",
					"description": _("Customer Group Heads."),
				},
				{
					"type": "doctype",
					"name": "SKU",
					"description": _("SKU"),
				},
            ]
        },
		{
			"label": _("Reports"),
			"items": [
            ]
        },
	]
