import os

import pandas as pd
from django.utils import timezone

from apps.forms.models import Submit
from config.celery import app


@app.task()
def download_xlsx(slug):
    data = (
        Submit.objects.filter(form__slug=slug).prefetch_related("form").values_list("id", "form", "form_title", "user")
    )
    df = pd.DataFrame(data=data)
    today_datetime = timezone.now().strftime("%Y%m%d_%H%M%S")
    directory = "/tmp/forms/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = f"submit_{slug}_{today_datetime}.xlsx"
    filepath = f"{directory}{filename}"
    df.to_excel(filepath, index=False)
    return filename
