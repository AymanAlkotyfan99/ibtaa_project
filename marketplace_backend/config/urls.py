"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", TemplateView.as_view(template_name="auth/register.html"), name="register"), # Placeholder for logic
    path("dashboard/", TemplateView.as_view(template_name="dashboard/index.html"), name="dashboard"),
    
    path("admin/", admin.site.urls),
    
    # Users & Auth
    path("api/", include("users.urls")),
    
    # Core Admin
    path("api/admin/", include("core.urls")),
    
    # Subscriptions (Shared)
    path("api/", include("subscriptions.urls")),
    
    # Marketplace (Customer & Merchant)
    path("api/merchant/", include("marketplace.urls")),
    path("api/customer/", include("marketplace.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
