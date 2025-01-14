from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Edu_Master.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = 'Edu_Master.views.error_404_view'