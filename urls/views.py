from django.views.generic import CreateView, DetailView, RedirectView, ListView
from django.shortcuts import get_object_or_404

from urls.models import Url


class UrlCreateView(CreateView):
    model = Url
    fields = ["original_url"]


class UrlDetailView(DetailView):
    model = Url
    slug_field = "url_identifier"
    slug_url_kwarg = "url_identifier"


class UrlRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url = get_object_or_404(Url, url_identifier=kwargs.get("url_identifier"))
        url.increment_access_count()
        return url.original_url


class TopUrlsListView(ListView):
    queryset = Url.objects.order_by("-access_count")[:100]
    context_object_name = "urls"
