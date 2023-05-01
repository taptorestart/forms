import factory
from django.contrib.auth.models import User
from factory import SubFactory

from apps.forms.models import Form, Component, Choice, Answer


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


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


class AnswerFactory(factory.django.DjangoModelFactory):
    component = SubFactory(ComponentFactory)

    class Meta:
        model = Answer
