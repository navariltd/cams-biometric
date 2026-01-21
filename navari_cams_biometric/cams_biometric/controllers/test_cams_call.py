from datetime import datetime
import json
import frappe
from frappe.tests.utils import FrappeTestCase
from unittest.mock import patch
from frappe import db
from navari_cams_biometric.cams_biometric.controllers.cams_call import (
    handle_attendance_log,
    handle_punch_logs,
    attendance,
    update_last_sync_time,
)


class TestCamsCall(FrappeTestCase):

    def test_handle_attendance_log_inserts_checkin(self):
        rawdata = json.dumps({
            "RealTime": {
                "PunchLog": {
                    "Type": "CheckIn",
                    "LogTime": "2024-05-01T08:00:00",
                    "UserId": "EMP001",
                    "InputType": "Fingerprint"
                }
            }
        })

        handle_attendance_log("STG001", rawdata)
        employee_id =  "EMP001"
        checkins = db.get_all("Employee Checkin", 
        filters=[
        ["employee", "=", employee_id],
        ["time", ">=", "2024-05-01 08:00:00"],
        ["time", "<", "2024-05-01 09:00:00"]
         ])


        self.assertEqual(len(checkins), 1)


    def test_handle_punch_logs_inserts_checkins(self):
        punch_logs = [{
            "Type": "CheckIn",
            "LogTime": "2024-05-01T08:00:00",
            "UserID": "EMP002",
            "InputType": "Fingerprint"
        }, {
            "Type": "CheckOut",
            "LogTime": "2024-05-01T17:00:00",
            "UserID": "EMP002",
            "InputType": "Fingerprint"
        }]


        handle_punch_logs("STG001", punch_logs)

        employee_id = "EMP002"
        checkins = db.get_all("Employee Checkin", 
        filters=[
        ["employee", "=", employee_id],
        ["time", ">=", "2024-05-01 08:00:00"],
        ["time", "<", "2024-05-01 18:00:00"]
         ])

        self.assertEqual(len(checkins), 2)

    @patch("navari_cams_biometric.cams_biometric.controllers.cams_call.handle_punch_logs")
    @patch("navari_cams_biometric.cams_biometric.controllers.cams_call.handle_attendance_log")
    @patch("navari_cams_biometric.cams_biometric.controllers.cams_call.frappe")
    def test_attendance_function(
        self,
        mock_frappe,
        mock_handle_attendance_log,
        mock_handle_punch_logs
    ):
        # Case 1: No rawdata
        mock_frappe.local.request.get_data.return_value = None
        mock_frappe.local.form_dict.get.return_value = None

        response = attendance()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(response.data, b'{"status": "done"}')

        # Case 2: Invalid JSON
        mock_frappe.local.request.get_data.return_value = "invalid json"
        response = attendance()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{"status": "done"}')

        # Case 3: RealTime CheckIn
        data_realtime = {
            "RealTime": {
                "PunchLog": {
                    "Type": "CheckIn",
                    "LogTime": "2025-05-29T09:00:00",
                    "UserId": "EMP001",
                    "InputType": "Fingerprint"
                }
            }
        }
        rawdata_realtime = json.dumps(data_realtime)
        mock_frappe.local.request.get_data.return_value = rawdata_realtime
        mock_frappe.local.form_dict.get.return_value = "STG001"

        response = attendance()
        self.assertEqual(response.status_code, 200)
        mock_handle_attendance_log.assert_called_once_with("STG001", rawdata_realtime)

        # Case 4: PunchLog CheckOut
        data_punchlog = {
            "PunchLog": {
                "Log": [{
                    "Type": "CheckOut",
                    "LogTime": "2025-05-29T17:00:00",
                    "UserID": "EMP001",
                    "InputType": "Fingerprint"
                }]
            }
        }
        rawdata_punchlog = json.dumps(data_punchlog)
        mock_frappe.local.request.get_data.return_value = rawdata_punchlog
        mock_frappe.local.form_dict.get.return_value = "STG001"

        response = attendance()
        self.assertEqual(response.status_code, 200)
        mock_handle_punch_logs.assert_called_once_with("STG001", data_punchlog["PunchLog"]["Log"])

    def test_update_last_sync_time_updates_field(self):
        if frappe.db.exists("Shift Type", "TEST_SHIFT"):
            frappe.delete_doc("Shift Type", "TEST_SHIFT", force=True)
            
        #dummy Shift Type
        shift_doc = frappe.get_doc({
            "doctype": "Shift Type",
            "name": "TEST_SHIFT",
            "start_time": "09:00:00",
            "end_time": "17:00:00"
        }).insert()

        
        test_time = datetime(2024, 6, 6, 10, 30)

        
        result = update_last_sync_time(shift_doc.name, test_time)

        updated_shift = frappe.get_doc("Shift Type", shift_doc.name)

        self.assertEqual(result, "done")
        self.assertEqual(updated_shift.last_sync_of_checkin, test_time)