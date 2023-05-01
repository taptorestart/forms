from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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

    def validate_answers(self, value):
        for data in value:
            component: Component = data.get("component")
            answer = data.get("answer")
            choice: Choice = data.get("choice")
            if component.is_text_question and component.is_required and answer is None:
                raise ValidationError({"answer": ["This field may not be blank."]})
            if component.is_select_question and component.is_required and choice is None:
                raise ValidationError({"choice": ["This field may not be blank."]})
        return value

    def validate(self, attrs):
        form: Form = attrs.get("form")
        answers = attrs.get("answers")
        form_components_ids = form.component_set.all().values_list("id", flat=True)
        components_required_ids = form.component_set.filter(is_required=True).values_list("id", flat=True)
        components_ids = [answer.get("component").id for answer in answers]
        if set(components_ids) - set(form_components_ids):
            raise ValidationError({"answers": ["Answers have invalid components."]})
        if set(components_required_ids) - set(components_ids):
            raise ValidationError({"answers": ["Answers don't have required components."]})
        return attrs
