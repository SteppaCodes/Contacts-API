from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("api/v1/schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/",SpectacularSwaggerView.as_view(url_name="schema")),
    
    path('back-dash/', admin.site.urls),
    path("api/v1/", include("apps.accounts.urls")),
    path("api/v1/", include("apps.contacts.urls"))
]
