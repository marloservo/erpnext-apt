# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns(filters)
    stock_entries = get_stock_entry_details(filters)

    data = []

    for se in stock_entries:
        temp_data = []
        if not filters.from_date:
            temp_data.append(se.date)
        temp_data.append(se.customer_group)
        temp_data.append(se.warehouse)
        temp_data.append(se.store_code)
        temp_data.append(se.item)
        temp_data.append(se.description)
        temp_data.append(se.sku)
        temp_data.append(se.upc)
        temp_data.append(se.dept_code)
        temp_data.append(se.qty)

        data.append(temp_data)

    return columns, data


def get_columns(filters=None):
    temp_data = []
    if not filters.from_date:
        temp_data.append(_("Date") + ":Date:95")
    temp_data.append(_("Customer Group") + ":Link/Customer Group:100")
    temp_data.append(_("Warehouse") + ":Link/Warehouse:250")
    temp_data.append(_("Code") + "::50")
    temp_data.append(_("Item") + ":Link/Item:100")
    temp_data.append(_("Description") + "::200")
    temp_data.append(_("SKU") + "::100")
    temp_data.append(_("UPC") + "::150")
    temp_data.append(_("Dept") + "::50")
    temp_data.append(_("Qty") + ":Int:50")

    return temp_data


def get_stock_entry_details(filters):
    return frappe.db.sql("""select date(se.posting_date) date,
            w.customer_group, se.to_warehouse warehouse, w.ppp_store_code store_code, 
            sed.item_code item, i.description, sk.sku_name sku, sk.upc, sk.dept_code,
            sum(sed.qty) qty
        from `tabStock Entry Detail` sed
        left join `tabStock Entry` se on se.name = sed.parent
        left join `tabWarehouse` w on w.name = se.to_warehouse
        left join `tabItem` i on i.name = sed.item_code
        left join `tabSKU` sk on sk.item = sed.item_code and sk.consignee = w.customer_group 
        where 
            {se_conditions}
        group by
            date(se.posting_date), w.customer_group, se.to_warehouse, w.ppp_store_code, 
            sed.item_code, i.description, sk.sku_name, sk.upc, sk.dept_code
        order by se.posting_date asc, se.posting_time asc, se.name asc""" \
                         .format(se_conditions=get_se_conditions(filters)), filters, as_dict=1)


def get_item_conditions(filters):
    conditions = []
    if filters.get("item_code"):
        conditions.append("name=%(item_code)s")
    if filters.get("brand"):
        conditions.append("brand=%(brand)s")

    return "where {}".format(" and ".join(conditions)) if conditions else ""


def get_se_conditions(filters):
    conditions = []
    if filters.from_date:
        conditions.append("se.posting_date=%(from_date)s")
    item_conditions = get_item_conditions(filters)
    if item_conditions:
        conditions.append("""se.item_code in (select name from tabItem
            {item_conditions})""".format(item_conditions=item_conditions))
    if filters.warehouse:
        conditions.append("se.to_warehouse=%(warehouse)s")
    if filters.stock_entry:
        conditions.append("sed.parent=%(stock_entry)s")
    if filters.sku:
        conditions.append("sk.name=%(sku)s")

    return "{}".format(" and ".join(conditions)) if conditions else ""


