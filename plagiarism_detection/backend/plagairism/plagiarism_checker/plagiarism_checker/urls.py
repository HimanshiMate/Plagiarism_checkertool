"""
URL configuration for plagiarism_checker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('checker.urls')),  # Include the checker app URLs
# ]

from django.contrib import admin
from django.urls import include, path



# from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    # path('api/detect-text/', views.detect_text, name='detect_text'),
    # path('api/detect-pdf/', views.detect_pdf, name='detect_pdf'),
    # path('api/detect-image/', views.detect_image, name='detect_image'),

    path('admin/', admin.site.urls),
    path('', include('checker.urls')),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)