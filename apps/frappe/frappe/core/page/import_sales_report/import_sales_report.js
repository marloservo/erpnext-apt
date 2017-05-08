//MARLO 20161027
// frappe.DataImportTool = Class.extend({
frappe.ImportSalesReport = Class.extend({
    init: function(parent) {
        
        this.page = frappe.ui.make_app_page({
            parent: parent,
            //MARLO 20161027
            // title: __("Data Import Tool"),            
            title: __("Upload Sales Report"),
            single_column: true
        });
        //MARLO 20161027
        // this.page.add_inner_button(__("Help"), function() {
        //    frappe.help.show_video("6wiriRKPhmg");
        // });
        this.make();
        this.make_upload();
        
        //MARLO 20161027
        this.select.val('Sales Invoice').change();
    },
    set_route_options: function() {
        var doctype = null;
        if(frappe.get_route()[1]) {
            doctype = frappe.get_route()[1];
        } else if(frappe.route_options && frappe.route_options.doctype) {
            doctype = frappe.route_options.doctype;
        }

        if(in_list(frappe.boot.user.can_import, doctype)) {
                this.select.val(doctype).change();
        }

        frappe.route_options = null;
    },
    make: function() {
        var me = this;
        frappe.boot.user.can_import = frappe.boot.user.can_import.sort();

        $(frappe.render_template("data_import_main", this)).appendTo(this.page.main);

        this.select = this.page.main.find("select.doctype");
        this.select_columns = this.page.main.find('.select-columns');
        this.select.on("change", function() {
            me.doctype = $(this).val();
            frappe.model.with_doctype(me.doctype, function() {
                me.page.main.find(".export-import-section").toggleClass(!!me.doctype);
                if(me.doctype) {

                    // render select columns
                    var doctype_list = [frappe.get_doc('DocType', me.doctype)];
                    frappe.meta.get_table_fields(me.doctype).forEach(function(df) {
                        doctype_list.push(frappe.get_doc('DocType', df.options));
                    });
                    
                    //MARLO 20161027
                    // remove other non-essential doctypes
                    var required_list = ['Sales Invoice', 'Sales Invoice Item'];
                    var new_list = [];
                    doctype_list.forEach( function(doctype) {
                        if( required_list.indexOf( doctype.name ) >= 0 ) {
                            new_list.push(doctype);
                        }
                    });
                    
                    //MARLO 20161027
                    // $(frappe.render_template("data_import_tool_columns", {doctype_list: doctype_list}))
                    $(frappe.render_template("data_import_tool_columns", {doctype_list: new_list}))
                        .appendTo(me.select_columns.empty());
                        
                    //MARLO 20161027
                    var unselect_button = me.page.main.find('.btn-unselect-all');
                    unselect_button.trigger('click');
                    me.select.prop('disabled', 'disabled');
                    me.page.main.find('[name="always_insert"]').prop('checked', true).prop("disabled", true);
                    me.page.main.find('[name="submit_after_import"]').prop('checked', true).prop("disabled", true);
                    me.page.main.find('[name="ignore_encoding_errors"]').prop('checked', false).prop("disabled", true);
                    
                    
                    //MARLO 20161108
                    //check only essential fields
                    var required_fields = ['naming_series', 'posting_date', 'company', 'currency', 'conversion_rate', 'selling_price_list', 'price_list_currency', 'plc_conversion_rate', 'base_net_total', 'base_grand_total', 'grand_total', 'debit_to', 'customer_group', 'store_code', 'due_date', 'update_stock', 'apply_discount_on', 'discount_amount', ' item_name', 'description', 'rate', 'amount', 'base_rate', 'base_amount', 'income_account', 'cost_center', 'item_code', 'qty', 'cashier', 'time_sold', 'sku'];
                    $.each( required_fields, function(i, fieldName) {
                        $("input[data-fieldname=" + fieldName + "]")[0].checked = true;
                    });
                    
                    //MARLO 20161108
                    //hide unnecessary options
                    unselect_button.parent().addClass("hide");
                    $("h4:contains('Columns')").addClass("hide");
                    $(".select-columns").addClass("hide");
                }                
            });
        });

        this.page.main.find('.btn-select-all').on('click', function() {
            me.select_columns.find('.select-column-check').prop('checked', true);
        });

        this.page.main.find('.btn-unselect-all').on('click', function() {
            me.select_columns.find('.select-column-check').prop('checked', false);
        });

        this.page.main.find('.btn-select-mandatory').on('click', function() {
            me.select_columns.find('.select-column-check').prop('checked', false);
            me.select_columns.find('.select-column-check[data-reqd="1"]').prop('checked', true);
        });

        this.page.main.find(".btn-download-template").on('click', function() {
            window.open(me.get_export_url(false));
        });

        this.page.main.find(".btn-download-data").on('click', function() {
            window.open(me.get_export_url(true));
        });

    },
    get_export_url: function(with_data) {
        var doctype = this.select.val();
        var columns = {};

        this.select_columns.find('.select-column-check:checked').each(function() {
            var _doctype = $(this).attr('data-doctype');
            var _fieldname = $(this).attr('data-fieldname');
            if(!columns[_doctype]) {
                columns[_doctype] = [];
            }
            columns[_doctype].push(_fieldname);
        });
        //MARLO 20161027
        // return "/api/method/frappe.core.page.data_import_tool.exporter.get_template?"
        return "/api/method/frappe.core.page.data_import_tool.exporter_custom.get_template?"
            + "doctype=" + doctype
            + "&parent_doctype=" + doctype
            + "&select_columns=" + JSON.stringify(columns)
            + "&with_data="+ (with_data ? 'Yes' : 'No')+"&all_doctypes=Yes";
    },
    make_upload: function() {
        var me = this;
        frappe.upload.make({
            parent: this.page.main.find(".upload-area"),
            btn: this.page.main.find(".btn-import"),
            get_params: function() {
                return {
                    submit_after_import: me.page.main.find('[name="submit_after_import"]').prop("checked"),
                    ignore_encoding_errors: me.page.main.find('[name="ignore_encoding_errors"]').prop("checked"),
                    overwrite: !me.page.main.find('[name="always_insert"]').prop("checked")
                }
            },
            args: {
                //MARLO 20161027
                // method: 'frappe.core.page.data_import_tool.importer.upload',
                method: 'frappe.core.page.data_import_tool.importer_custom.upload',
            },
            onerror: function(r) {
                me.onerror(r);
            },
            queued: function() {
                // async, show queued
                msg_dialog.clear();
                msgprint(__("Import Request Queued. This may take a few moments, please be patient."));
            },
            running: function() {
                // update async status as running
                msg_dialog.clear();
                msgprint(__("Importing..."));
                me.write_messages([__("Importing")]);
                me.has_progress = false;
            },
            progress: function(data) {
                // show callback if async
                if(data.progress) {
                    frappe.hide_msgprint(true);
                    me.has_progress = true;
                    frappe.show_progress(__("Importing"), data.progress[0],
                        data.progress[1]);
                }
            },
            callback: function(attachment, r) {
                if(r.message.error || r.message.messages.length==0) {
                    me.onerror(r);
                } else {
                    if(me.has_progress) {
                        frappe.show_progress(__("Importing"), 1, 1);
                        setTimeout(frappe.hide_progress, 1000);
                    }

                    r.messages = ["<h5 style='color:green'>" + __("Import Successful!") + "</h5>"].
                        concat(r.message.messages)

                    me.write_messages(r.messages);
                }
            },
            is_private: true
        });

        frappe.realtime.on("data_import_progress", function(data) {
            if(data.progress) {
                frappe.hide_msgprint(true);
                me.has_progress = true;
                frappe.show_progress(__("Importing"), data.progress[0],
                    data.progress[1]);
            }
        })

    },
    write_messages: function(data) {
        this.page.main.find(".import-log").removeClass("hide");
        var parent = this.page.main.find(".import-log-messages").empty();

        // TODO render using template!
        for (var i=0, l=data.length; i<l; i++) {
            var v = data[i];
            var $p = $('<p></p>').html(frappe.markdown(v)).appendTo(parent);
            if(v.substr(0,5)=='Error') {
                $p.css('color', 'red');
            } else if(v.substr(0,8)=='Inserted') {
                $p.css('color', 'green');
            } else if(v.substr(0,7)=='Updated') {
                $p.css('color', 'green');
            } else if(v.substr(0,5)=='Valid') {
                $p.css('color', '#777');
            }
        }
    },
    onerror: function(r) {
        if(r.message) {
            // bad design: moves r.messages to r.message.messages
            r.messages = $.map(r.message.messages, function(v) {
                var msg = v.replace("Inserted", "Valid")
                    .replace("Updated", "Valid").split("<");
                if (msg.length > 1) {
                    v = msg[0] + (msg[1].split(">").slice(-1)[0]);
                } else {
                    v = msg[0];
                }
                return v;
            });

            r.messages = ["<h4 style='color:red'>" + __("Import Failed") + "</h4>"]
                .concat(r.messages);

            r.messages.push("Please correct the format of the file and import again.");

            frappe.show_progress(__("Importing"), 1, 1);

            this.write_messages(r.messages);
        }
    }
});

//MARLO 20161027
// frappe.pages['data-import-tool'].on_page_load = function(wrapper) {
//     frappe.data_import_tool = new frappe.DataImportTool(wrapper);
// }
//
// frappe.pages['data-import-tool'].on_page_show = function(wrapper) {
//     frappe.data_import_tool && frappe.data_import_tool.set_route_options();
// }

frappe.pages['import-sales-report'].on_page_load = function(wrapper) {
    frappe.import_sales_report = new frappe.ImportSalesReport(wrapper);
}

frappe.pages['import-sales-report'].on_page_show = function(wrapper) {
    frappe.import_sales_report && frappe.import_sales_report.set_route_options();
}
