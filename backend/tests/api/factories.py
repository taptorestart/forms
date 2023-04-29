import factory
from factory import SubFactory

from apps.forms.models import Form, Component, Choice


class FormFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Form


class ComponentFactory(factory.django.DjangoModelFactory):
    form = SubFactory(FormFactory)

    class Meta:
        model = Component


class ChoiceFactory(factory.django.DjangoModelFactory):
    component = SubFactory(ComponentFactory)

    class Meta:
        model = Choice
