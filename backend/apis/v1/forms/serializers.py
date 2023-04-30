from rest_framework import serializers

from apps.forms.models import Form, Component, Choice, Submit, Answer


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
