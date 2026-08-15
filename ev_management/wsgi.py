
"""
WSGI configuration for the AI EV Management System.

This module exposes the WSGI application used to run or deploy
the Django backend of the AI EV Management System.

The Django backend handles EV data, traffic-management APIs,
charging-station information, and other server-side services.

Project settings are loaded from:
    ev_management.settings
"""

import os

from django.core.wsgi import get_wsgi_application


# Tell Django which settings file should be used.
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "ev_management.settings"
)


# Create the WSGI application used by the web server.
application = get_wsgi_application()
