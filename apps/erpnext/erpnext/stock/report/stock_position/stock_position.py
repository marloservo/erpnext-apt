# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns(filters)
    sl_entries = get_stock_ledger_entries(filters)
    item_details = get_item_details(filters)
    
    data = []
    for sle in sl_entries:
        item_detail = item_details[sle.item_code]
        
        temp_data = []
        if not filters.warehouse :
            temp_data.append(sle.warehouse)
        temp_data.append(sle.item_code)
        temp_data.append(item_detail.description)
        temp_data.append(item_detail.brand)
        temp_data.append(item_detail.stock_uom)
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
            sle.item_code, sle.warehouse, sle.qty_after_transaction, sle.valuation_rate, sle.stock_value
        from `tabStock Ledger Entry` sle
        inner join (
            select max( name ) name, warehouse, item_code
            from  `tabStock Ledger Entry` 
            where date( posting_date ) <=  %(to_date)s
            group by warehouse, item_code
            ) a on a.name = sle.name
        where 1=1
            {sle_conditions}
            """\
        .format(sle_conditions=get_sle_conditions(filters)), filters, as_dict=1)

def get_item_details(filters):
    item_details = {}
    for item in frappe.db.sql("""select name, item_name, description, item_group,
            brand, stock_uom from `tabItem` {item_conditions}"""\
            .format(item_conditions=get_item_conditions(filters)), filters, as_dict=1):
        item_details.setdefault(item.name, item)

    return item_details

def get_item_conditions(filters):
    conditions = []
    if filters.get("item_code"):
        conditions.append("name=%(item_code)s")
    if filters.get("brand"):
        conditions.append("brand=%(brand)s")

    return "where {}".format(" and ".join(conditions)) if conditions else ""

def get_sle_conditions(filters):
    conditions = []
    item_conditions=get_item_conditions(filters)
    if item_conditions:
        conditions.append("""sle.item_code in (select name from tabItem
            {item_conditions})""".format(item_conditions=item_conditions))
    if filters.warehouse:
        conditions.append(get_warehouse_condition(filters.get("warehouse")))

    return "and {}".format(" and ".join(conditions)) if conditions else ""
    
def get_warehouse_condition(warehouse):
    warehouse_details = frappe.db.get_value("Warehouse", warehouse, ["lft", "rgt"], as_dict=1)
    if warehouse_details:
        return " exists (select name from `tabWarehouse` wh \
            where wh.lft >= %s and wh.rgt <= %s and sle.warehouse = wh.name)"%(warehouse_details.lft,
            warehouse_details.rgt)

    return ''
