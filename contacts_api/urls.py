from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/",SpectacularSwaggerView.as_view(url_name="schema")),
    
    path('admin/', admin.site.urls),
    path("api/", include("apps.accounts.urls"))
]
