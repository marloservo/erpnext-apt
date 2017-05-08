frappe.listview_settings['Customer'] = {
	add_fields: ["customer_name", "customer_group", "store_code", "status"],
	get_indicator: function(doc) {
		color = {
			'Open': 'red',
			'Active': 'green',
			'Dormant': 'darkgrey'
		}
		return [__(doc.status), color[doc.status], "status,=," + doc.status];
	}

};
