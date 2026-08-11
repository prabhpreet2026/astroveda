"""
URL configuration for astro project.

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
from myapp import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("index",views.index, name="index"),
    path("about",views.about, name="about"),
    
    path("four_zero_four",views.four_zero_four, name="four_zero_four"),
    path("blog",views.blog, name="blog"),
    path("blog_details",views.blog_details, name="blog_details"),
    path("contact",views.contact, name="contact"),
    path("footer",views.footer, name="footer"),
    path("faq",views.faq, name="faq"),
    path("navbar",views.navbar, name="navbar"),
    path("pricing",views.pricing, name="pricing"),
    path("services/", views.services, name="services"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("appointment/", views.appointment, name="appointment"),
    path("payment/", views.dummy_payment, name="dummy_payment"),
    path("payment/success/", views.dummy_payment_success, name="dummy_payment_success"),
    path("payment/failed/", views.dummy_payment_failed, name="dummy_payment_failed"),
]
