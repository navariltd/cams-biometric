import json
from dateutil import parser

import frappe
from frappe import _
from flask import Response

from ...utils import logger


@frappe.whitelist(allow_guest=True)
def attendance():
    rawdata = frappe.local.request.get_data(as_text=True)
    stgid = frappe.local.form_dict.get("stgid")

    logger.info(f"Raw data received: {rawdata}")
    logger.info(f"STGID: {stgid}")

    data = []

    if not rawdata:
        return Response(
            json.dumps({"status": "done"}), status=200, mimetype="application/json"
        )

    try:
        data = json.loads(rawdata)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return Response(
            json.dumps({"status": "done"}), status=200, mimetype="application/json"
        )

    if "RealTime" in data:
        handle_attendance_log(stgid, rawdata)
    elif "PunchLog" in data:
        handle_punch_logs(stgid, data["PunchLog"]["Log"])

    return Response(
        json.dumps({"status": "done"}), status=200, mimetype="application/json"
    )


def handle_attendance_log(stgid, rawdata):
    if not rawdata:
        return

    try:
        request_data = json.loads(rawdata)
        punch_log = request_data.get("RealTime", {}).get("PunchLog", {})


        device_id = punch_log.get("UserId")
        log_time = punch_log.get("LogTime")
        log_type_punch = punch_log.get("Type")
        input_type = punch_log.get("InputType")

        employee = frappe.db.get_value(
            "Employee",
            filters={"attendance_device_id": device_id, "status": "Active"},
        )

        if not employee:
            frappe.log_error(
                "Missing Employee",
                f"Cams Biometric Error No Employee with device UserID {device_id} found."
            )
            return

        log_type = "OUT" if log_type_punch == "CheckOut" else "IN"

        # Convert the datetime format using dateutil.parser
        log_time_dt = parser.parse(log_time)
        formatted_log_time = log_time_dt.strftime("%Y-%m-%d %H:%M:%S")

        default_shift = get_shift(device_id)
        
        # Check if the employee check-in already exists
        existing_checkin = frappe.db.exists(
            "Employee Checkin",
            {
                "employee": employee,
                "time": formatted_log_time,
                "log_type": log_type,
            },
        )

        if existing_checkin:
            logger.warning(f"Duplicate check-in detected: {existing_checkin}")
            return

        # Storing the values in Employee Checking doctype
        employee_checking = frappe.get_doc(
            {
                "doctype": "Employee Checkin",
                "employee": employee,
                "time": formatted_log_time,
                "custom_constant_time": formatted_log_time,
                "log_type": log_type,
                "shift": default_shift,
                "custom_input_type": input_type,
                "punch_type": log_type_punch,
            }
        )

        employee_checking.insert(ignore_permissions=True)
        frappe.db.commit()

        logger.info(f"Successfully created check-in: {employee_checking.name}")

        if default_shift:
            update_last_sync_time(default_shift, formatted_log_time)

    except Exception as e:
        logger.error(f"Error in handle_attendance_log: {e}", exc_info=True)
        frappe.log_error(
            "Attendance Log Error",
            f"Error processing attendance log: {str(e)}\nData: {rawdata}"
        )

    finally:
        return "done"


@frappe.whitelist(allow_guest=True)
def handle_punch_logs(stgid, punch_logs):
    if not punch_logs:
        return

    device_ids = [log.get("UserID") for log in punch_logs]
    employees = frappe.get_all(
        "Employee",
        filters={"attendance_device_id": ["in", device_ids], "status": "Active"},
        fields=["name", "attendance_device_id"],
    )

    if not employees:
        title = _("Cams Biometric Error")
        msg = _("No Employee with Attendance Device ID found")
        logger.error(msg)
        frappe.log_error(title, msg)
        return

    emp_map = {emp.attendance_device_id: emp.name for emp in employees}

    for punch_log in punch_logs:
        employee_id = emp_map.get(punch_log.get("UserID"))
        if not employee_id:
            logger.warning(f"Unknown device UserID {punch_log.get('UserID')} in punch log; skipping entry.")
            frappe.log_error(
                "Cams Biometric Error"
                f"Unknown device UserID {punch_log.get('UserID')} in punch log; skipping entry."
            )
            continue
        
        try:
            log_type_punch = punch_log["Type"]
            log_type = "OUT" if log_type_punch == "CheckOut" else "IN"

            # Convert the datetime format using dateutil.parser
            log_time = punch_log["LogTime"]
            log_time_dt = parser.parse(log_time)
            formatted_log_time = log_time_dt.strftime("%Y-%m-%d %H:%M:%S")
            default_shift = get_shift(punch_log["UserID"])
            # Check if the employee check-in already exists
            existing_checkin = frappe.db.exists(
                "Employee Checkin",
                {
                    "employee": employee_id,
                    "time": formatted_log_time,
                    "log_type": log_type,
                },
            )

            if existing_checkin:
                logger.warning(f"Duplicate check-in: {existing_checkin}")
                continue

            # Storing the values in Employee Checkin doctype
            employee_checking = frappe.get_doc(
                {
                    "doctype": "Employee Checkin",
                    "employee": employee_id,
                    "time": formatted_log_time,
                    "custom_constant_time": formatted_log_time,
                    "log_type": log_type,
                    "custom_input_type": punch_log.get("InputType"),
                    "shift": default_shift,
                }
            )

            employee_checking.insert(ignore_permissions=True)
            frappe.db.commit()
            if default_shift:
                update_last_sync_time(default_shift, formatted_log_time)

        except Exception as e:
            logger.error(f"Error processing punch log: {str(e)}", exc_info=True)
            continue

    return "done"


def add_user():
    first_name = frappe.form_dict.get("first_name")
    last_name = frappe.form_dict.get("last_name")
    user_id = frappe.form_dict.get("user_id")
    user_type = frappe.form_dict.get("user_type")


def delete_user():
    user_id = frappe.form_dict.get("user_id")
    user_type = frappe.form_dict.get("user_type")


def add_photo():
    user_id = frappe.form_dict.get("user_id")
    user_type = frappe.form_dict.get("user_type")
    photo = frappe.form_dict.get("photo")


def load_punch_logs():
    pass


def get_shift(biometric_id):
    user = frappe.db.sql(
        """
        SELECT name, default_shift 
        FROM `tabEmployee`
        WHERE attendance_device_id = %s
    """,
        (biometric_id,),
        as_dict=True,
    )
    frappe.flags.ignore_permissions = False  # Reset permissions

    if user:
        return user[0].get("default_shift")
    return None


def update_last_sync_time(shift, time):
    frappe.db.set_value(
        "Shift Type", shift, "last_sync_of_checkin", time, update_modified=False
    )
    frappe.db.commit()
    return "done"


# Constant Time is a data field just added for informational purpose only. It is not used in any calculation or logic. It is just a copy of the time field.
# The time field is the actual time of the punch log.
# It is important when you want to view different zone but maintain the time of the original zone.
