from django.conf.urls.i18n import i18n_patterns

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from config.settings import (
    STATIC_URL,
    STATIC_ROOT,
    MEDIA_URL,
    MEDIA_ROOT,
)

urlpatterns = (
        [
            path('api/v1/', include('config.v1_urls')),
        ]
        + i18n_patterns(path('admin/', admin.site.urls), )
        + static(STATIC_URL, document_root=STATIC_ROOT)
        + static(MEDIA_URL, document_root=MEDIA_ROOT)
)
