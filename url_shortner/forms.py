from django import forms

from url_shortner.models import Url


class UrlForm(forms.ModelForm):
    class Meta:
        model = Url
        fields = ("original_url",)
