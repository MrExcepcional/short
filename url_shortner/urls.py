from django.urls import path

from url_shortner import views

app_name = "url_shortner"

urlpatterns = [
    path("", views.UrlCreateView.as_view(), name="create"),
    path("top/", views.TopUrlsListView.as_view(), name="top-urls"),
    path("<slug:url_identifier>/", views.UrlDetailView.as_view(), name="detail"),
]
