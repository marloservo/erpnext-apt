from frappe import _

def get_data():
    return [
        {
            "label": _("Maintenance"),
            "icon": "icon-wrench",
            "items": [
                {
                    "type": "doctype",
                    "name": "User",
                    "description": _("User Maintenance"),
                },
                {
                    "type": "page",
                    "name": "permission-manager",
                    "label": _("Role Permissions"),
                },
            ]
        },
        {
            "label": _("Setup"),
            "icon": "icon-cog",
            "items": [
                {
                    "type": "doctype",
                    "name": "Accounts Settings",
                    "description": _("Default settings for accounting transactions.")
                },
                {
                    "type": "doctype",
                    "name": "Stock Settings",
                    "label": "Global Stock Settings",
                    "description": _("Default settings for stock transactions.")
                },
                {
                    "type": "doctype",
                    "name": "Fiscal Year",
                    "description": _("Financial / accounting year.")
                },
                {
                    "type": "doctype",
                    "name": "Currency",
                    "description": _("Enable / disable currencies.")
                },
                {
                    "type": "doctype",
                    "name": "Currency Exchange",
                    "description": _("Currency exchange rate master.")
                },
                {
                    "type": "doctype",
                    "name":"Terms and Conditions",
                    "label": _("Terms and Conditions Template"),
                    "description": _("Template of terms or contract.")
                },
                {
                    "type": "doctype",
                    "name":"Mode of Payment",
                    "description": _("e.g. Bank, Cash, Credit Card")
                },
            ]
        },
    ]