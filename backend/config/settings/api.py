from config.settings.base import *


ROOT_URLCONF = "config.urls.api"


INSTALLED_APPS += [
    "rest_framework",
    "drf_spectacular",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Form API",
    "DESCRIPTION": "Form API Documentation",
    "VERSION": "1.0.0",
    "SWAGGER_UI_SETTINGS": {
        "docExpansion": "list",
        "defaultModelRendering": "example",
        "defaultModelExpandDepth": 10,
        "defaultModelsExpandDepth": 10,
        "deepLinking": True,
        "displayRequestDuration": True,
        "persistAuthorization": True,
        "syntaxHighlight.activate": True,
    },
}
