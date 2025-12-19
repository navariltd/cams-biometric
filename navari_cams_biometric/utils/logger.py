import frappe

_LOGGER_NAME = "cams_biometric"


def _get_logger():
    logger = frappe.logger(
        _LOGGER_NAME,
        allow_site=True,
        file_count=10,
    )
    logger.setLevel("INFO")

    return logger


def info(message, *args):
    _get_logger().info(message, *args)


def debug(message, *args):
    if frappe.conf.get("cams_debug"):
        _get_logger().debug(message, *args)


def warning(message, *args):
    _get_logger().warning(message, *args)


def error(message, *args):
    _get_logger().error(message, *args)
