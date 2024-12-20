"""
URL configuration for spa_service project.

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
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from comment.captcha_views import get_captcha, validate_captcha

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/users/",
        include("user.urls", namespace="user-api")
    ),
    path(
        "api/v1/comments/",
        include("comment.urls", namespace="comment-api")
    ),
    path("api/v1/get-captcha/", get_captcha, name="get-captcha"),
    path("api/v1/validate-captcha/", validate_captcha, name="validate-captcha"),
    path("captcha/", include("captcha.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += debug_toolbar_urls()
