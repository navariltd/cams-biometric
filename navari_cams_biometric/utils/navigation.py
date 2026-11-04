"""Desk visibility for the standalone CAMS Biometric app."""

import frappe


def has_cams_access():
    """Allow HR operators and system administrators into the CAMS app."""
    return bool(
        {"HR User", "HR Manager", "System Manager"}
        & set(frappe.get_roles(frappe.session.user))
    )
