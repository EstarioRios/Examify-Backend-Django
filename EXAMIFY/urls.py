from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Uncomment if you want the admin:
    # path("admin/", admin.site.urls),
    
    path("auth/", include("AuthenticationSystem.urls")),
]
