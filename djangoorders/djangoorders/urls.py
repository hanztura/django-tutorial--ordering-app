"""djangoorders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from customers import views as customer_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/new/', customer_views.customer_create, name="customer_create"),
    path('customers/t/', customer_views.customer_table, name="customer_table"),
    path('customers/<int:pk>/', customer_views.customer_detail,
         name="customer_detail"),
    path('customers/<int:pk>/edit', customer_views.customer_update,
         name="customer_update"),
    path('customers/', customer_views.customer_list, name="customer_list"),
    path('', customer_views.home, name="home"),
]
