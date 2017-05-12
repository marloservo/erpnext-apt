// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["Barcode"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
		},
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse"
		},
		{
			"fieldname":"brand",
			"label": __("Brand"),
			"fieldtype": "Link",
			"options": "Brand"
		},
		{
			"fieldname":"item_code",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname":"sku",
			"label": __("SKU"),
			"fieldtype": "Link",
			"options": "SKU"
		},
		{
			"fieldname":"stock_entry",
			"label": __("TR#"),
			"fieldtype": "Link",
			"options": "Stock Entry"
		},
	]
}
