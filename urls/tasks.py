import requests

from bs4 import BeautifulSoup

from gettingstarted import celery_app


@celery_app.task(bind=True)
def extract_title_from_url(self, url_id):
    from urls.models import Url

    url = Url.objects.filter(id=url_id).first()

    if url:
	    response = requests.get(url.original_url)
	    soup = BeautifulSoup(response.content, "html.parser")

	    url.title = soup.title.string
	    url.save()
