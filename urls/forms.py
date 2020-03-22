from django import forms

from urls.models import Url


class UrlForm(forms.ModelForm):
    class Meta:
        model = Url
        fields = ("original_url",)
