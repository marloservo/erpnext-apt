from frappe import _

data = {
	'heatmap': True,
	'heatmap_message': _('This is based on stock movement. See {0} for details')\
		.format('<a href="#query-report/Stock Ledger">' + _('Stock Ledger') + '</a>'),
	'fieldname': 'item_code',
	'non_standard_fieldnames': {
		'Production Order': 'production_item',
		'Product Bundle': 'new_item_code',
		'BOM': 'item',
		'Batch': 'item',
        'SKU': 'item',
	},
	'transactions': [
        # MARLO 20161209 CUSTOMIZE LINKS
		{
			'label': _('Sell'),
			'items': ['Sales Invoice', 'Item Price', 'SKU']
		},
		{
			'label': _('Buy'),
			'items': ['Purchase Invoice']
		},
		{
			'label': _('Move'),
			'items': ['Stock Entry']
		},
	]
	# 'transactions': [
		# {
			# 'label': _('Groups'),
			# 'items': ['BOM', 'Product Bundle']
		# },
		# {
			# 'label': _('Pricing'),
			# 'items': ['Item Price', 'Pricing Rule']
		# },
		# {
			# 'label': _('Sell'),
			# 'items': ['Quotation', 'Sales Order', 'Delivery Note', 'Sales Invoice']
		# },
		# {
			# 'label': _('Buy'),
			# 'items': ['Material Request', 'Supplier Quotation', 'Request for Quotation',
				# 'Purchase Order', 'Purchase Invoice']
		# },
		# {
			# 'label': _('Traceability'),
			# 'items': ['Serial No', 'Batch']
		# },
		# {
			# 'label': _('Move'),
			# 'items': ['Stock Entry']
		# },
		# {
			# 'label': _('Manufacture'),
			# 'items': ['Production Order']
		# }
	# ]    
}