"""
URL configuration for tobacco_app project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.http import HttpResponse

def robots_txt(request):
    content = """User-agent: *
Allow: /
Sitemap: https://tobaccoleafclassification.online/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', include('classifier.urls')),
    path('robots.txt', robots_txt),
]

# Add URL patterns for serving media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
