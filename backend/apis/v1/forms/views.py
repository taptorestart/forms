from rest_framework import permissions, mixins
from rest_framework.viewsets import GenericViewSet

from apis.v1.forms.serializers import FormRetrieveSerializer, FormSerializer, ComponentSerializer, ChoiceSerializer
from apps.forms.models import Form, Component, Choice


class FormViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Form.objects.all()
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ["post", "get", "patch", "delete"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FormRetrieveSerializer
        return FormSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            return (permissions.AllowAny(),)
        return (permissions.IsAdminUser(),)


class ComponentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Component.objects.all()
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
