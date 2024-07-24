// Copyright (c) 2024, Navari Limited and contributors
// For license information, please see license.txt
let loader = document.createElement("div");
loader.className = "loader";
loader.style.display = "none";

document.body.appendChild(loader);

let css =
  ".loader { border: 8px solid #f3f3f3; border-top: 8px solid #3498db; border-radius: 50%; width: 40px; height: 40px; margin-left: 50%; position: fixed; bottom: 50% ; animation: spin 2s linear infinite; } @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }";

let style = document.createElement("style");
style.appendChild(document.createTextNode(css));
document.head.appendChild(style);

frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        if(frm.doc.custom_biometric_registered===0)
        {
        frm.add_custom_button(__('Register Biometric ID'), function() {
            let d = new frappe.ui.Dialog({
                title: 'Add Biometric ID',
                fields: [
                    {
                        label: 'First Name',
                        fieldname: 'first_name',
                        fieldtype: 'Data',
                        reqd: 1,
                        default: frm.doc.first_name
                    },
                    {
                        label: 'Last Name',
                        fieldname: 'last_name',
                        fieldtype: 'Data',
                        reqd: 1,
                        default: frm.doc.last_name
                    },
                    {
                        label: 'Biometric ID',
                        fieldname: 'user_id',
                        fieldtype: 'Data',
                        reqd: 1,
                        default:frm.doc.attendance_device_id
                    },
                    {
                        label: 'User Type',
                        fieldname: 'user_type',
                        fieldtype: 'Select',
                        options: [
                            { label: 'User', value: 'User' },
                            { label: 'Administrator', value: 'Administrator' }
                        ],
                        default: 'User',
                        reqd: 1
                    }
                ],
                primary_action_label: 'Add User',
                primary_action: function(data) {
                    d.hide();
                    loader.style.display = "block";
                    frappe.call({
                        method: 'navari_frappehr_biostar.controllers.cams_call.add_user',
                        args: {
                            first_name: data.first_name,
                            last_name: data.last_name,
                            user_id: data.user_id,
                            user_type: data.user_type
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
    }

        if(frm.doc.custom_biometric_registered===1){

        
        frm.add_custom_button(__('Delete Biometric ID'), function() {
            let d = new frappe.ui.Dialog({
                title: 'Delete Biometric ID',
                fields: [
                    {
                        label: 'Biometric ID',
                        fieldname: 'user_id',
                        fieldtype: 'Data',
                        reqd: 1,
                        default: frm.doc.attendance_device_id,
                    }
                ],
                primary_action_label: 'Delete User',
                primary_action: function(data) {
                    d.hide();
                    loader.style.display = "block";
                    frappe.call({
                        method: 'navari_frappehr_biostar.controllers.cams_call.delete_user',
                        args: {
                            user_id: data.user_id
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
        }).addClass("btn-danger");
    }

        frm.add_custom_button(__('Add Photo'), function() {
            let d = new frappe.ui.Dialog({
                title: 'Add Photo',
                fields: [
                    {
                        label: 'Biometric ID',
                        fieldname: 'user_id',
                        fieldtype: 'Data',
                        reqd: 1
                    },
                    {
                        label: 'Photo',
                        fieldname: 'photo',
                        fieldtype: 'Attach Image',
                        reqd: 1
                    }
                ],
                primary_action_label: 'Upload Photo',
                primary_action: function(data) {
                    d.hide();
                    loader.style.display = "block";
                    frappe.call({
                        method: 'navari_frappehr_biostar.controllers.cams_call.add_photo',
                        args: {
                            user_id: data.user_id,
                            photo: data.photo
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
        }).addClass("btn-secondary");

    }
});
