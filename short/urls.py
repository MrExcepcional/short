from django.urls import path, include
from django.contrib import admin
from django.shortcuts import redirect

from urls.views import UrlRedirectView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", lambda request: redirect("/urls/")),
    path("urls/", include("urls.urls", namespace="urls")),
    path("<str:url_identifier>", UrlRedirectView.as_view(), name="redirect"),
]
