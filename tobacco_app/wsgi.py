"""
WSGI config for tobacco_app project.
"""

import os
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tobacco_app.settings')

application = get_wsgi_application()

# Wrap with WhiteNoise for static files (default prefix /static/)
application = WhiteNoise(application, root=settings.STATIC_ROOT, prefix='static/')

# Add media file serving under /media/
application.add_files(settings.MEDIA_ROOT, prefix='media/')