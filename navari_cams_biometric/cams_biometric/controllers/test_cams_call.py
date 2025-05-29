import json
from unittest import TestCase
from unittest.mock import patch, MagicMock
from navari_cams_biometric.cams_biometric.controllers.cams_call import (
    handle_attendance_log,
    handle_punch_logs,
    attendance,
)


class TestCamsCall(TestCase):

    @patch("navari_cams_biometric.cams_biometric.controllers.cams_call.frappe")
    @patch("navari_cams_biometric.cams_biometric.controllers.cams_call.parser")
    def test_handle_attendance_log_inserts_checkin(self, mock_parser, mock_frappe):
        rawdata = '''
        {
            "RealTime": {
                "PunchLog": {
                    "Type": "CheckIn",
                    "LogTime": "2024-05-01T08:00:00",
                    "UserId": "EMP001",
                    "InputType": "Fingerprint"
                }
            }
        }
        '''

        mock_parser.parse.return_value.strftime.return_value = "2024-05-01 08:00:00"
        mock_frappe.db.exists.return_value = None
        mock_frappe.get_doc.return_value.insert.return_value = None
        mock_frappe.db.commit = MagicMock()
        mock_frappe.db.sql.return_value = [{"default_shift": "Shift A"}]

        handle_attendance_log("STG001", rawdata)

        self.assertEqual(mock_frappe.get_doc.call_count, 1)
        self.assertEqual(mock_frappe.db.commit.call_count, 2)

    @patch("navari_cams_biometric.cams_biometric.controllers.cams_call.frappe")
    @patch("navari_cams_biometric.cams_biometric.controllers.cams_call.parser")
    def test_handle_punch_logs_inserts_checkins(self, mock_parser, mock_frappe):
        punch_logs = [{
            "Type": "CheckIn",
            "LogTime": "2024-05-01T08:00:00",
            "UserID": "EMP001",
            "InputType": "Fingerprint"
        }, {
            "Type": "CheckOut",
            "LogTime": "2024-05-01T17:00:00",
            "UserID": "EMP001",
            "InputType": "Fingerprint"
        }]

        mock_parser.parse.return_value.strftime.return_value = "2024-05-01 08:00:00"
        mock_frappe.db.exists.return_value = None
        mock_frappe.get_doc.return_value.insert.return_value = None
        mock_frappe.db.commit = MagicMock()
        mock_frappe.db.sql.return_value = [{"default_shift": "Shift A"}]

        handle_punch_logs("STG001", punch_logs)

        self.assertEqual(mock_frappe.get_doc.call_count, 2)
        self.assertEqual(mock_frappe.db.commit.call_count, 4)

    @patch("navari_cams_biometric.cams_biometric.controllers.cams_call.frappe")
    @patch("navari_cams_biometric.cams_biometric.controllers.cams_call.handle_attendance_log")
    @patch("navari_cams_biometric.cams_biometric.controllers.cams_call.handle_punch_logs")
    def test_attendance_function(self, mock_handle_punch_logs, mock_handle_attendance_log, mock_frappe):
        mock_frappe.local.request.get_data.return_value = ''
        mock_frappe.local.form_dict.get.return_value = None

        response = attendance()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(response.data, b'{"status": "done"}')
        mock_handle_attendance_log.assert_not_called()
        mock_handle_punch_logs.assert_not_called()

        mock_frappe.local.request.get_data.return_value = 'invalid json'
        mock_frappe.local.form_dict.get.return_value = None

        response = attendance()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(response.data, b'{"status": "done"}')
        mock_handle_attendance_log.assert_not_called()
        mock_handle_punch_logs.assert_not_called()

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


