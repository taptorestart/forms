from django.urls import include, path

urlpatterns = [
    path("v1/", include("apis.v1.urls")),
]
