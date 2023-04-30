from rest_framework import serializers

from apps.forms.models import Form, Component, Choice, Submit, Answer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "component", "text", "order"]


class ComponentSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(source="choice_set", many=True, required=False)

    class Meta:
        model = Component
        fields = ["id", "form", "type", "title", "description", "order", "choices"]
        read_only_fields = ["choices"]


class FormSerializer(serializers.ModelSerializer):
    components = ComponentSerializer(source="component_set", many=True, required=False)

    class Meta:
        model = Form
        fields = ["id", "slug", "title", "start_date", "end_date", "components"]
        read_only_fields = ["components"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["component", "question_title", "answer", "choice", "choice_text"]
        read_only_fields = ["submit", "question_title", "choice_text"]


class SubmitSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, allow_null=True)

    class Meta:
        model = Submit
        fields = ["id", "form", "form_title", "user", "answers"]
        read_only_fields = ["form_title", "user"]
