from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apis.v1.forms.serializers import (
    FormSerializer,
    ComponentSerializer,
    ChoiceSerializer,
    SubmitSerializer,
)
from apps.forms.models import Form, Component, Choice, Answer, Submit


class FormViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Form.objects.all().prefetch_related("component_set", "component_set__choice_set")
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ["post", "get", "patch", "delete"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "submit":
            return SubmitSerializer
        return FormSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve", "submit"]:
            return (permissions.AllowAny(),)
        return (permissions.IsAdminUser(),)

    @action(detail=True, methods=["post"])
    def submit(self, request, slug=None):
        form = get_object_or_404(Form, slug=slug)
        serializer = SubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answers = serializer.validated_data.get("answers")
        answer_list = []
        user = None if type(request.user) == AnonymousUser else request.user
        submit = Submit.objects.create(form=form, form_title=form.title, user=user)
        for answer in answers:
            answer_list.append(
                Answer(
                    submit=submit,
                    component=answer.get("component"),
                    question_title=answer.get("component").title if answer.get("component") else "",
                    answer=answer.get("answer") if answer.get("answer") else "",
                    choice=answer.get("choice"),
                    choice_text=answer.get("choice").text if answer.get("choice") else "",
                )
            )
        Answer.objects.bulk_create(answer_list)
        return Response(status=status.HTTP_201_CREATED)


class ComponentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Component.objects.all().prefetch_related("choice_set")
    serializer_class = ComponentSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ["post", "get", "patch", "delete"]

    def get_queryset(self):
        return Component.objects.filter(form__slug=self.kwargs.get("form_slug"))


class ChoiceViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ["post", "get", "patch", "delete"]

    def get_queryset(self):
        return Choice.objects.filter(component_id=self.kwargs.get("component_pk"))
