// Copyright (c) 2024, Navari Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on("Cams Biometric Settings", {
	refresh(frm) {

        frm.add_custom_button(__('Load Punchlog'), function() {
            let d = new frappe.ui.Dialog({
                title: 'Load Punchlog',
                fields: [
                    {
                        label: 'Biometric ID',
                        fieldname: 'user_id',
                        fieldtype: 'Data',
                        reqd: 1
                    },
                    {
                        label: 'Start Date',
                        fieldname: 'start_date',
                        fieldtype: 'Date',
                        reqd: 1
                    },
                    {
                        label: 'End Date',
                        fieldname: 'end_date',
                        fieldtype: 'Date',
                        reqd: 1
                    }
                ],
                primary_action_label: 'Load Punchlogs',
                primary_action: function(data) {
                    d.hide();
                    loader.style.display = "block";
                    frappe.call({
                        method: 'navari_frappehr_biostar.controllers.cams_call.load_punch_logs',
                        args: {
                            user_id: data.user_id,
                            start_date: data.start_date,
                            end_date: data.end_date
                        },
                        callback: function(r) {
                            loader.style.display = "none";
                            if (r.message) {
                                frappe.msgprint(r.message);
                            }
                        }
                    });
                }
            });
            d.show();
        }).addClass("btn-primary");
	},


});

