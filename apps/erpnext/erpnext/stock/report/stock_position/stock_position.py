# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns(filters)
    sl_entries = get_stock_ledger_entries(filters)

    data = []
    for sle in sl_entries:
        temp_data = []
        if not filters.warehouse:
            temp_data.append(sle.warehouse)
        temp_data.append(sle.item_code)
        temp_data.append(sle.description)
        temp_data.append(sle.brand)
        temp_data.append(sle.stock_uom)
        temp_data.append(sle.qty_after_transaction)
        temp_data.append(sle.stock_value)
        
        data.append(temp_data)
            
    return columns, data

def get_columns(filters=None):
    temp_data = []
    if not filters.warehouse :
        temp_data.append(_("Warehouse") + ":Link/Warehouse:300")
    temp_data.append(_("Item") + ":Link/Item:100")
    temp_data.append(_("Description") + "::200")
    temp_data.append(_("Brand") + ":Link/Brand:100") 
    temp_data.append(_("UOM") + ":Link/UOM:75")
    temp_data.append(_("Balance Qty") + ":Int:100")
    temp_data.append(_("Balance Value") + ":Currency:110")
        
    return temp_data

def get_stock_ledger_entries(filters):
    return frappe.db.sql("""select date(sle.posting_date) date,
            sle.item_code, sle.warehouse, sle.qty_after_transaction, sle.stock_value,
            i.description, i.brand, i.stock_uom
        from `tabStock Ledger Entry` sle
        inner join (
            select max( name ) name, warehouse, item_code
            from  `tabStock Ledger Entry` 
            where date( posting_date ) <=  %(to_date)s
              and warehouse = %(warehouse)s
            group by warehouse, item_code
            ) a on a.name = sle.name
        left join `tabItem` i on i.name = sle.item_code
        where 1=1
            {sle_conditions}
            """\
        .format(sle_conditions=get_sle_conditions(filters)), filters, as_dict=1)

def get_sle_conditions(filters):
    conditions = []
    if filters.item_code:
        conditions.append("sle.item_code=%(item_code)s")
    if filters.warehouse:
        conditions.append("sle.warehouse=%(warehouse)s")
    if filters.brand:
        conditions.append("i.brand=%(brand)s")

    return "and {}".format(" and ".join(conditions)) if conditions else ""
    
