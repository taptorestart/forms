from datetime import datetime, time

import pytest
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from apps.forms.models import Component
from tests.apis.factories import ComponentFactory
from tests.apis.factories import FormFactory


@pytest.fixture
def form():
    start_date = datetime.combine(timezone.now().replace(day=1), time.min)
    end_date = datetime.combine(timezone.now().replace(day=1) + relativedelta(months=1), time.max)
    form = FormFactory(slug="test", title="Form test", start_date=start_date, end_date=end_date)
    return form


@pytest.fixture
def form_abc():
    start_date = datetime.combine(timezone.now().replace(day=1), time.min)
    end_date = datetime.combine(timezone.now().replace(day=1) + relativedelta(months=1), time.max)
    form = FormFactory(slug="abc", title="Form abc", start_date=start_date, end_date=end_date)
    return form


@pytest.fixture()
def component_radio(form):
    component: Component = ComponentFactory(form=form, type=Component.RADIO, is_required=True)
    return component


@pytest.fixture()
def component_select(form):
    component: Component = ComponentFactory(form=form, type=Component.SELECT, is_required=True)
    return component


@pytest.fixture()
def component_checkbox(form):
    component: Component = ComponentFactory(form=form, type=Component.CHECKBOX, is_required=True)
    return component


@pytest.fixture()
def component_text(form):
    component: Component = ComponentFactory(form=form, type=Component.TEXT, is_required=True)
    return component
