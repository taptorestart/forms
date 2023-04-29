from django.urls import include, path
from rest_framework_nested import routers

from apis.v1.forms.views import FormViewSet, ComponentViewSet, ChoiceViewSet

router = routers.SimpleRouter()
router.register(r"forms", viewset=FormViewSet, basename="form")

forms_router = routers.NestedSimpleRouter(router, r"forms", lookup="form")
forms_router.register(r"components", ComponentViewSet, basename="component")

components_router = routers.NestedSimpleRouter(forms_router, r"components", lookup="component")
components_router.register(r"choices", ChoiceViewSet, basename="choice")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(forms_router.urls)),
    path("", include(components_router.urls)),
]
