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

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        if start_date and end_date and end_date < start_date:
            raise ValidationError({"end_date": ["The end date cannot be earlier than the start date."]})
        return attrs


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
        component_to_choice = {}
        for data in value:
            component: Component = data.get("component")
            answer = data.get("answer")
            choice: Choice = data.get("choice")
            if component.is_select_one_question and component_to_choice.get(component.id):
                raise ValidationError({"component": ["Select only one choice."]})
            if component.is_select_one_question and not component_to_choice.get(component.id) and choice:
                component_to_choice[component.id] = choice.id

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
