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
from ninja import NinjaAPI
from ninja.security import HttpBearer
from accounts.api import router as accounts_router
from hr.api import router as hr_router

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token

api = NinjaAPI(auth=GlobalAuth(), csrf=True)  # CSRF保護を有効化

api.add_router("/v1/", accounts_router, tags = ["Test"])
api.add_router("/v1/", hr_router, tags = ["Hr"])

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]
