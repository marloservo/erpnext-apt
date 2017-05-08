# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SKU(Document):
    # MARLO 20161214
    def before_insert(self):
        # Check existing SKU for Consignee / Customer Group
        # Create a new Item if not existing
        # Require fields for New Item
        
        
        # if not self.item_name or not self.standard_rate or not self.stock_uom:
            # frappe.throw("Description/Name, Standard Price, and UOM is required for New Items")
        
        # if not frappe.db.exists("Item", {"item_name" : self.item_name, "standard_rate": self.standard_rate}):
            # # CREATE A NEW ITEM
            # new_item = frappe.get_doc({
                # "doctype": "Item",
                # "item_name": self.item_name,
                # "stock_uom": self.stock_uom,
                # "standard_rate": self.standard_rate,
                # "is_stock_item": 1,
                # "naming_series": "I-",
                # "is_sales_item": 1,
                # "is_purchase_item": 1
            # })
            # new_item.name = self.sku_name
            # new_item.insert()
            # self.item = new_item.name
        # else:
            # self.item = frappe.db.get_value("Item", {"item_name" : self.item_name, "standard_rate": self.standard_rate}, "name")
                
        self.create_pricelist()
                
    def after_insert(self):
        self.create_item_price()
    
    def autoname(self):
        # MARLO 20161215
        self.name = self.consignee + "-" + self.sku_name
        
    def on_update(self):
        #MARLO 20161216
        self.create_pricelist()
        self.create_item_price()
        
    def create_pricelist(self):
        # Create a Price List if Not Existing
        # Include The Consignee Rate for this particular item/sku
        if self.consignee:
            existing_price_list = frappe.db.get_value("Price List", self.consignee, "price_list_name")
            if not existing_price_list:
                new_price_list = frappe.get_doc({
                    "doctype": "Price List",
                    "customer_group": self.consignee,
                    "price_list_name": self.consignee,
                    "selling": 1,
                    "currency": "PHP",
                    "enabled": 1
                })
                new_price_list.insert()

    def create_item_price(self):
        if self.group_rate:
            if not frappe.db.exists("Item Price", {"sku" : self.name, "selling": 1}):
                item_name, item_brand = frappe.db.get_value("Item", self.item, ["item_name", "brand"])                
                new_rate = frappe.get_doc({
                    "doctype": "Item Price",
                    "price_list": self.consignee,
                    "sku": self.name,
                    "item_code": self.item,
                    "selling": 1,
                    "customer_group": self.consignee,
                    "price_list_rate": self.group_rate,
                    "item_name": item_name,
                    "item_description": item_name,
                    "brand": item_brand,
                    "currency": "PHP",
                })
                new_rate.insert()
            else:
                existing_rate = frappe.get_doc("Item Price", {"sku" : self.name, "selling": 1})
                existing_rate.update({"price_list_rate" : self.group_rate})
                existing_rate.save()
    