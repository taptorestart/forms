from django.urls import include, path
from rest_framework import routers

from apis.v1.forms.views import FormViewSet

router = routers.DefaultRouter()
router.register(r"forms", FormViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
