from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls.static import static

urlpatterns = [
    path("api/v1/schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/", SpectacularSwaggerView.as_view(url_name="schema"), name='api-home'),
    path("api/back-dash/", admin.site.urls),
    path("api/v1/", include("apps.accounts.urls")),
    path("api/v1/", include("apps.contacts.urls")),
    path("api/v1/", include("apps.favourites.urls")),
    path("api/v1/", include("apps.groups.urls")),
    path('', include("apps.common.urls"))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
