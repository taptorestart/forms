import os
from dataclasses import dataclass
from typing import Optional

import pandas as pd
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from pandas import DataFrame

from apps.forms.models import Submit, Form, Component
from config.celery import app


@app.task()
def download_xlsx(slug: str) -> str:
    df = get_dataframe(slug)
    today_datetime = timezone.now().strftime("%Y%m%d_%H%M%S")
    directory = "/tmp/forms/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = f"submit_{slug}_{today_datetime}.xlsx"
    filepath = f"{directory}{filename}"
    df.to_excel(filepath, index=False)
    return filename


@dataclass
class Column:
    index: int
    name: str
    component_id: Optional[int]


def get_dataframe(slug: str) -> DataFrame:
    form = Form.objects.get(slug=slug)
    component_qs = Component.objects.filter(form=form.id, type__in=Component.QUESTION_TYPES).order_by("order")
    columns = []
    column_values = {0: _("created at"), 1: _("user")}
    start_index = 2
    max_index = start_index + len(component_qs)
    for index, component in enumerate(component_qs):
        columns.append(Column(index=start_index + index, name=component.title, component_id=component.id))
    for column in columns:
        column_values[column.index] = column.name
    column_list = [column_values[i] if i in column_values else None for i in range(max_index)]

    submit_qs = Submit.objects.filter(form__slug=slug)
    data = []
    rows = []
    for submit in submit_qs:
        answers = submit.answer_set.all().prefetch_related("component")
        row = {0: submit.created_at.strftime("%Y-%m-%d %H:%M:%S"), 1: submit.user.username if submit.user else None}
        for answer in answers:
            column_index = next((c.index for c in columns if c.component_id == answer.component_id), None)
            answer_text = ""
            if answer.component.type in Component.QUESTION_SELECT_TYPES:
                answer_text = answer.choice_text
            if answer.component.type in Component.QUESTION_TEXT_TYPES:
                answer_text = answer.answer
            if column_index not in row:
                row[column_index] = answer_text
            else:
                row[column_index] += "\n" + answer_text
        rows.append(row)
    for row in rows:
        row_data = [row.get(i) for i in range(max_index)]
        data.append(row_data)
    df = pd.DataFrame(data=data, columns=column_list)
    return df
