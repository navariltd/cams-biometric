import json
import frappe
from frappe import _
from dateutil import parser
from flask import Response 

@frappe.whitelist(allow_guest=True)
def attendance():
    rawdata = frappe.local.request.get_data(as_text=True)
    stgid = frappe.local.form_dict.get('stgid')
    print(f"Received data: {rawdata}")  # Print raw data for debugging

    if not rawdata:
        return Response(
            json.dumps({"status": "done"}),
            status=200,
            mimetype='application/json'
        )

    try:
        data = json.loads(rawdata)
    except json.JSONDecodeError as e:
        return Response(
            json.dumps({"status": "done"}),
            status=200,
            mimetype='application/json'
        )

    if "RealTime" in data:
        handle_attendance_log(stgid, rawdata)
    elif "PunchLog" in data:
        handle_punch_logs(stgid, data["PunchLog"]["Log"])

    return Response(
        json.dumps({"status": "done"}),
        status=200,
        mimetype='application/json'
    )

def handle_attendance_log(stgid, rawdata):
    request_data = json.loads(rawdata)

    log_type_punch = request_data["RealTime"]["PunchLog"]["Type"]
    log_type = 'OUT' if log_type_punch == 'CheckOut' else 'IN'

    # Convert the datetime format using dateutil.parser
    log_time = request_data["RealTime"]["PunchLog"]["LogTime"]
    log_time_dt = parser.parse(log_time)
    formatted_log_time = log_time_dt.strftime("%Y-%m-%d %H:%M:%S")

    # Check if the employee check-in already exists
    existing_checkin = frappe.db.exists("Employee Checkin", {
        "employee": request_data["RealTime"]["PunchLog"]["UserId"],
        "time": formatted_log_time,
        "log_type": log_type
    })

    if not existing_checkin:
        # Storing the values in Employee Checking doctype
        employee_checking = frappe.get_doc({
            "doctype": "Employee Checkin",
            "employee": request_data["RealTime"]["PunchLog"]["UserId"],
            "time": formatted_log_time,
            "log_type": log_type,
            "custom_input_type": request_data["RealTime"]["PunchLog"]["InputType"]
        })

        employee_checking.insert(ignore_permissions=True)
        frappe.db.commit()

    return "done"

def handle_punch_logs(stgid, punch_logs):
    for punch_log in punch_logs:
        log_type_punch = punch_log["Type"]
        log_type = 'OUT' if log_type_punch == 'CheckOut' else 'IN'

        # Convert the datetime format using dateutil.parser
        log_time = punch_log["LogTime"]
        log_time_dt = parser.parse(log_time)
        formatted_log_time = log_time_dt.strftime("%Y-%m-%d %H:%M:%S")

        # Check if the employee check-in already exists
        existing_checkin = frappe.db.exists("Employee Checkin", {
            "employee": punch_log["UserID"],
            "time": formatted_log_time,
            "log_type": log_type
        })

        if not existing_checkin:
            # Storing the values in Employee Checkin doctype
            employee_checking = frappe.get_doc({
                "doctype": "Employee Checkin",
                "employee": punch_log["UserID"],
                "time": formatted_log_time,
                "log_type": log_type,
                "custom_input_type": punch_log["InputType"]
            })

            employee_checking.insert(ignore_permissions=True)
            frappe.db.commit()

    return "done"

def add_user():
    first_name=frappe.form_dict.get('first_name')
    last_name=frappe.form_dict.get('last_name')
    user_id=frappe.form_dict.get('user_id')
    user_type=frappe.form_dict.get('user_type')
    
def delete_user():
    user_id=frappe.form_dict.get('user_id')
    user_type=frappe.form_dict.get('user_type')
    
def add_photo():
    user_id=frappe.form_dict.get('user_id')
    user_type=frappe.form_dict.get('user_type')
    photo=frappe.form_dict.get('photo')
    
def load_punch_logs():
    pass
