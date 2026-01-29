from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Frontend Routes
    path('', include('apps.frontend.urls')),
    path('members/', include('apps.members.urls')),
    path('inventory/', include('apps.inventory.urls')),
]