from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework import status

from apis.v1.forms.serializers import FormSerializer, ChoiceSerializer, ComponentSerializer, SubmitSerializer

EXAMPLE_RESPONSE_403_FORBIDDEN = OpenApiExample(
    response_only=True,
    summary="forbidden",
    name="forbidden",
    value={"detail": "Authentication credentials were not provided."},
    status_codes=[status.HTTP_403_FORBIDDEN],
)
EXAMPLE_RESPONSE_404_NOT_FOUND = OpenApiExample(
    response_only=True,
    summary="Not found",
    name="Not found",
    value={"detail": "Not found."},
    status_codes=[status.HTTP_404_NOT_FOUND],
)
RESPONSE_204_NO_CONTENT = OpenApiResponse(response=None, description="No Content")
RESPONSE_403_FORBIDDEN = OpenApiResponse(response=OpenApiTypes.ANY, description="Forbidden")
RESPONSE_404_NOT_FOUND = OpenApiResponse(response=OpenApiTypes.ANY, description="Not Found")


SWAGGER_FORM_TAGS = ["forms"]
SCHEMA_FORM_LIST = extend_schema(
    tags=SWAGGER_FORM_TAGS,
    summary="get form list",
    operation_id="get form list",
    examples=[
        EXAMPLE_RESPONSE_404_NOT_FOUND,
    ],
    responses={
        200: OpenApiResponse(response=FormSerializer(many=True), description="OK"),
        404: RESPONSE_404_NOT_FOUND,
    },
)
SCHEMA_FORM_CREATE = extend_schema(
    tags=SWAGGER_FORM_TAGS,
    summary="create form",
    operation_id="create form",
    examples=[
        EXAMPLE_RESPONSE_403_FORBIDDEN,
        EXAMPLE_RESPONSE_404_NOT_FOUND,
    ],
    responses={
        200: OpenApiResponse(response=FormSerializer, description="OK"),
        403: RESPONSE_403_FORBIDDEN,
        404: RESPONSE_404_NOT_FOUND,
    },
)
SCHEMA_FORM_RETRIEVE = extend_schema(
    tags=SWAGGER_FORM_TAGS,
    summary="retrieve form",
    operation_id="retrieve form",
    examples=[
        EXAMPLE_RESPONSE_404_NOT_FOUND,
    ],
    responses={
        200: OpenApiResponse(response=FormSerializer, description="OK"),
        404: RESPONSE_404_NOT_FOUND,
    },
)
SCHEMA_FORM_PARTIAL_UPDATE = extend_schema(
    tags=SWAGGER_FORM_TAGS,
    summary="partial update form",
    operation_id="partial update form",
    examples=[
        EXAMPLE_RESPONSE_403_FORBIDDEN,
        EXAMPLE_RESPONSE_404_NOT_FOUND,
    ],
    responses={
        200: OpenApiResponse(response=FormSerializer, description="OK"),
        403: RESPONSE_403_FORBIDDEN,
        404: RESPONSE_404_NOT_FOUND,
    },
)
SCHEMA_FORM_DESTROY = extend_schema(
    tags=SWAGGER_FORM_TAGS,
    summary="delete form",
    operation_id="delete form",
    examples=[
        EXAMPLE_RESPONSE_403_FORBIDDEN,
        EXAMPLE_RESPONSE_404_NOT_FOUND,
    ],
    responses={
        204: RESPONSE_204_NO_CONTENT,
        403: RESPONSE_403_FORBIDDEN,
        404: RESPONSE_404_NOT_FOUND,
    },
)
SCHEMA_FORM_SUBMIT = extend_schema(
    tags=SWAGGER_FORM_TAGS,
    summary="submit form",
    operation_id="submit form",
    examples=[
        EXAMPLE_RESPONSE_404_NOT_FOUND,
    ],
    responses={
        200: OpenApiResponse(response=SubmitSerializer, description="OK"),
        404: RESPONSE_404_NOT_FOUND,
    },
)

SWAGGER_COMPONENT_TAGS = ["forms - components"]
SCHEMA_COMPONENT_LIST = extend_schema(
    tags=SWAGGER_COMPONENT_TAGS,
    summary="get component list",
    operation_id="get component list",
    examples=[
        EXAMPLE_RESPONSE_403_FORBIDDEN,
        EXAMPLE_RESPONSE_404_NOT_FOUND,
    ],
    responses={
        200: OpenApiResponse(response=ComponentSerializer(many=True), description="OK"),
        403: RESPONSE_403_FORBIDDEN,
        404: RESPONSE_404_NOT_FOUND,
    },
)
SCHEMA_COMPONENT_CREATE = extend_schema(
    tags=SWAGGER_COMPONENT_TAGS,
    summary="create component",
    operation_id="create component",
    examples=[
        EXAMPLE_RESPONSE_403_FORBIDDEN,
        EXAMPLE_RESPONSE_404_NOT_FOUND,
    ],
    responses={
        200: OpenApiResponse(response=ComponentSerializer, description="OK"),
        403: RESPONSE_403_FORBIDDEN,
        404: RESPONSE_404_NOT_FOUND,
    },
)
SCHEMA_COMPONENT_RETRIEVE = extend_schema(
    tags=SWAGGER_COMPONENT_TAGS,
    summary="retrieve component",
    operation_id="retrieve component",
    examples=[
        EXAMPLE_RESPONSE_403_FORBIDDEN,
        EXAMPLE_RESPONSE_404_NOT_FOUND,
    ],
    responses={
        200: OpenApiResponse(response=ComponentSerializer, description="OK"),
        403: RESPONSE_403_FORBIDDEN,
        404: RESPONSE_404_NOT_FOUND,
    },
)
SCHEMA_COMPONENT_PARTIAL_UPDATE = extend_schema(
    tags=SWAGGER_COMPONENT_TAGS,
    summary="partial update component",
    operation_id="partial update component",
    examples=[
        EXAMPLE_RESPONSE_403_FORBIDDEN,
        EXAMPLE_RESPONSE_404_NOT_FOUND,
    ],
    responses={
        200: OpenApiResponse(response=ComponentSerializer, description="OK"),
        403: RESPONSE_403_FORBIDDEN,
        404: RESPONSE_404_NOT_FOUND,
    },
)
SCHEMA_COMPONENT_DESTROY = extend_schema(
    tags=SWAGGER_COMPONENT_TAGS,
    summary="delete component",
    operation_id="delete component",
    examples=[
        EXAMPLE_RESPONSE_403_FORBIDDEN,
        EXAMPLE_RESPONSE_404_NOT_FOUND,
    ],
    responses={
        204: RESPONSE_204_NO_CONTENT,
        403: RESPONSE_403_FORBIDDEN,
        404: RESPONSE_404_NOT_FOUND,
    },
)

SWAGGER_CHOICE_TAGS = ["forms - components - choices"]
SCHEMA_CHOICE_LIST = extend_schema(
    tags=SWAGGER_CHOICE_TAGS,
    summary="get choice list",
    operation_id="get choice list",
    examples=[
        EXAMPLE_RESPONSE_403_FORBIDDEN,
        EXAMPLE_RESPONSE_404_NOT_FOUND,
    ],
    responses={
        200: OpenApiResponse(response=ChoiceSerializer(many=True), description="OK"),
        403: RESPONSE_403_FORBIDDEN,
        404: RESPONSE_404_NOT_FOUND,
    },
)
SCHEMA_CHOICE_CREATE = extend_schema(
    tags=SWAGGER_CHOICE_TAGS,
    summary="create choice",
    operation_id="create choice",
    examples=[
        EXAMPLE_RESPONSE_403_FORBIDDEN,
        EXAMPLE_RESPONSE_404_NOT_FOUND,
    ],
    responses={
        200: OpenApiResponse(response=ChoiceSerializer, description="OK"),
        403: RESPONSE_403_FORBIDDEN,
        404: RESPONSE_404_NOT_FOUND,
    },
)
SCHEMA_CHOICE_RETRIEVE = extend_schema(
    tags=SWAGGER_CHOICE_TAGS,
    summary="retrieve choice",
    operation_id="retrieve choice",
    examples=[
        EXAMPLE_RESPONSE_403_FORBIDDEN,
        EXAMPLE_RESPONSE_404_NOT_FOUND,
    ],
    responses={
        200: OpenApiResponse(response=ChoiceSerializer, description="OK"),
        403: RESPONSE_403_FORBIDDEN,
        404: RESPONSE_404_NOT_FOUND,
    },
)
SCHEMA_CHOICE_PARTIAL_UPDATE = extend_schema(
    tags=SWAGGER_CHOICE_TAGS,
    summary="partial update choice",
    operation_id="partial update choice",
    examples=[
        EXAMPLE_RESPONSE_403_FORBIDDEN,
        EXAMPLE_RESPONSE_404_NOT_FOUND,
    ],
    responses={
        200: OpenApiResponse(response=ChoiceSerializer, description="OK"),
        403: RESPONSE_403_FORBIDDEN,
        404: RESPONSE_404_NOT_FOUND,
    },
)
SCHEMA_CHOICE_DESTROY = extend_schema(
    tags=SWAGGER_CHOICE_TAGS,
    summary="delete choice",
    operation_id="delete choice",
    examples=[
        EXAMPLE_RESPONSE_403_FORBIDDEN,
        EXAMPLE_RESPONSE_404_NOT_FOUND,
    ],
    responses={
        204: RESPONSE_204_NO_CONTENT,
        403: RESPONSE_403_FORBIDDEN,
        404: RESPONSE_404_NOT_FOUND,
    },
)
