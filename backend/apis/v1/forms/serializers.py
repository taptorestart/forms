from rest_framework import serializers

from apps.forms.models import Form, Component, Choice


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ["id", "form", "type", "title", "description", "order"]


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ["id", "slug", "title", "start_date", "end_date"]


class FormRetrieveSerializer(serializers.ModelSerializer):
    components = ComponentSerializer(many=True, allow_null=True)

    class Meta:
        model = Form
        fields = ["id", "slug", "title", "start_date", "end_date", "components"]


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "component", "text"]
