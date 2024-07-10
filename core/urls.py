from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('home.urls')),  # Include home app URLs
    path('admin/', admin.site.urls),  # Default Django admin URLs
    # path('', include('admin_soft.urls')),  # Comment this line if using default Django admin
]
