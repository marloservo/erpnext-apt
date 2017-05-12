# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns(filters)
    sl_entries = get_stock_ledger_entries(filters)
    opening_row = get_opening_balance(filters, columns)
    
    data = []
    if opening_row:
        data.append(opening_row)

    for sle in sl_entries:
        temp_data = []
        temp_data.append(sle.date)
        if not filters.warehouse :
            temp_data.append(sle.warehouse)
        temp_data.append(sle.actual_qty if sle.actual_qty > 0 else '')
        temp_data.append(-sle.actual_qty if sle.actual_qty < 0 else '')
        temp_data.append(sle.actual_qty if sle.ppp_is_adjustable else '')
        temp_data.append(sle.qty_after_transaction)
        temp_data.append(sle.stock_value)
        if not filters.item_code:
            temp_data.append(sle.item_code)
            temp_data.append(sle.description)
        temp_data.append(sle.voucher_no)
        temp_data.append(sle.voucher_type)
        
        data.append(temp_data)
            
    return columns, data

def get_columns(filters=None):
    temp_data = []
    temp_data.append(_("Date") + ":Date:95")
    if not filters.warehouse:
        temp_data.append(_("Target Warehouse") + ":Link/Warehouse:250")
    temp_data.append(_("In") + ":Int:75")
    temp_data.append(_("Out") + ":Int:75")
    temp_data.append(_("Pending") + ":Int:75")
    temp_data.append(_("Balance Qty") + ":Int:100")
    temp_data.append(_("Balance Value") + ":Currency:110")
    if not filters.item_code :
        temp_data.append(_("Item") + ":Link/Item:100")
        temp_data.append(_("Description") + "::200")
    temp_data.append(_("Reference #") + ":Dynamic Link/" + _("Voucher Type") + ":100")
    temp_data.append(_("Voucher Type") + "::100")
        
    return temp_data

def get_stock_ledger_entries(filters):
    return frappe.db.sql("""select date(sle.posting_date) date,
            sle.item_code, sle.warehouse, sle.actual_qty, sle.qty_after_transaction, sle.incoming_rate, sle.valuation_rate,
            sle.stock_value, sle.voucher_type, sle.voucher_no, i.item_description
        from `tabStock Ledger Entry` sle
        left join `tabItem` i on i.name = sle.item_code
        where 
            sle.posting_date between %(from_date)s and %(to_date)s
            {sle_conditions}
            order by sle.posting_date asc, sle.posting_time asc, sle.name asc"""\
        .format(sle_conditions=get_sle_conditions(filters)), filters, as_dict=1)

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
    if item_conditions :
        conditions.append("""sle.item_code in (select name from tabItem
            {item_conditions})""".format(item_conditions=item_conditions))
    if filters.warehouse :
        conditions.append(get_warehouse_condition(filters.get("warehouse")))
    if filters.voucher_no :
        conditions.append("voucher_no=%(voucher_no)s")

    return "and {}".format(" and ".join(conditions)) if conditions else ""

def get_opening_balance(filters, columns):
    if not (filters.item_code and filters.warehouse and filters.from_date):
        return

    from erpnext.stock.stock_ledger import get_previous_sle
    last_entry = get_previous_sle({
        "item_code": filters.item_code,
        "warehouse": filters.warehouse,
        "posting_date": filters.from_date,
        "posting_time": "00:00"
    })
    
    idx_qty = 4
    idx_stock_value = 5
    idx_description = 6
            
    row = [""]*len(columns)
    row[idx_description] = _("Opening")
    if not last_entry :
        row[idx_qty] = 0
        row[idx_stock_value] = 0
    else :
        for i, v in ((idx_qty, 'qty_after_transaction'), (idx_stock_value, 'stock_value')):
                row[i] = last_entry.get(v, 0)
        
    return row
    
def get_warehouse_condition(warehouse):
    warehouse_details = frappe.db.get_value("Warehouse", warehouse, ["lft", "rgt"], as_dict=1)
    if warehouse_details:
        return " exists (select name from `tabWarehouse` wh \
            where wh.lft >= %s and wh.rgt <= %s and sle.warehouse = wh.name)"%(warehouse_details.lft,
            warehouse_details.rgt)

    return ''
