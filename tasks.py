from django.db import transaction, OperationalError

from justworktrial.celery import app
from pages.models import Page, Video, Audio, Text


@app.task(autoretry_for=(OperationalError,), retry_backoff=True, max_retries=5)
@transaction.atomic
def update_page_content_counters(page_id):
    models = (Video, Audio, Text)
    page = Page.objects.get(id=page_id)

    for model in models:
        objects = getattr(page, f'{model._meta.model_name}s').all()
        for o in objects:
            o.counter += 1
        model.objects.bulk_update(objects, ['counter'])
