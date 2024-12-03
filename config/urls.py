"""
URL configuration for config project.

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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static  # mediaを使うために追加
from ninja import NinjaAPI
from ninja.security import HttpBearer
from ninja_jwt.authentication import JWTAuth
from accounts.api import router as accounts_router
from hr.api import router as hr_router

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token

api = NinjaAPI(auth=JWTAuth(), csrf=True)  # CSRF保護を有効化

api.add_router("/v1/auth/", accounts_router, tags = ["Authentication"])
api.add_router("/v1/hr/", hr_router, tags = ["Hr"])

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]

if settings.DEBUG:
    # print("settings"+settings)
    print(f"settings: {settings.DEBUG}")
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 追加