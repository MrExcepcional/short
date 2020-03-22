from django.urls import path

from urls import views

app_name = "urls"

urlpatterns = [
    path("", views.UrlCreateView.as_view(), name="create"),
    path("top/", views.TopUrlsListView.as_view(), name="top-urls"),
    path("<slug:url_identifier>/", views.UrlDetailView.as_view(), name="detail"),
]
