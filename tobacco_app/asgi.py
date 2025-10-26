"""
ASGI config for tobacco_app project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tobacco_app.settings')

application = get_asgi_application()
