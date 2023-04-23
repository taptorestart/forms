from rest_framework import viewsets, permissions

from apis.v1.forms.serializers import FormSerializer
from apps.forms.models import Form


class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [permissions.AllowAny]
