frappe.listview_settings['Stock Entry'] = {
    add_fields: ["`tabStock Entry`.`name`", "`tabStock Entry`.`to_warehouse`", "`tabStock Entry`.`posting_date`"],
    column_render: {
        "from_warehouse": function(doc) {
            var html = "";
             if(doc.from_warehouse) {
                html += '<span class="filterable h6"\
                    data-filter="from_warehouse,=,'+doc.from_warehouse+'">'+doc.from_warehouse+' </span>';
            }
            if(doc.from_warehouse || doc.to_warehouse) {
                html += '<i class="octicon octicon-arrow-right text-muted"></i> ';
            }
            if(doc.to_warehouse) {
                html += '<span class="filterable h6"\
                data-filter="to_warehouse,=,'+doc.to_warehouse+'">'+doc.to_warehouse+'</span>';
            }
            return html;
        },
    },
	get_indicator: function(doc) {
        switch(doc.docstatus) {
            case 0 :   return [__("D"), "orange", "docstatus,=,0"];
                    break;
                    
            case 1 :   return [__("O"), "blue", "docstatus,=,1"];
                    break;
                    
            case 2 :   return [__("C"), "red", "docstatus,=,2"];
                    break;
        }
	},
    colwidths: {"subject": 4, "indicator": 2},
};
