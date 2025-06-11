import frappe
from frappe.utils import getdate, add_days

def execute(filters=None):
    yesterday = add_days(getdate(), -1)

    columns = [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee"},
        {"label": "Date", "fieldname": "date", "fieldtype": "Date"},
        {"label": "Issue", "fieldname": "issue", "fieldtype": "Data"},
    ]

    employees = frappe.get_all("Employee", fields=["name", "employee_name"])
    data = []

    for emp in employees:
        checkins = frappe.get_all("Employee Checkin", filters={
            "employee": emp.name,
            "log_date": yesterday
        }, fields=["log_type"])

        log_types = {log.log_type for log in checkins}
        if "IN" not in log_types:
            data.append({"employee": emp.name, "date": yesterday, "issue": "Missing IN"})
        elif "OUT" not in log_types:
            data.append({"employee": emp.name, "date": yesterday, "issue": "Missing OUT"})

    return columns, data
