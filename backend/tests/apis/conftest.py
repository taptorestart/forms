import importlib
import json
from types import NoneType

import pytest
from django.contrib.auth.models import User
from pytest_bdd import given, parsers, when, then
from rest_framework.test import APIClient

from tests.apis.factories import UserFactory


@pytest.fixture
def client_anonymous():
    client: APIClient = APIClient()
    return client


@pytest.fixture
def client_staff():
    user_staff: User = UserFactory(username="staff", is_staff=True)
    client: APIClient = APIClient()
    client.force_authenticate(user=user_staff)
    return client


DATA_TYPES = {
    "bool": bool,
    "int": int,
    "str": str,
    "float": float,
    "list": list,
    "tuple": tuple,
    "dict": dict,
    "NoneType": NoneType,
}


@given(parsers.parse("I am a/an {user_type} user."), target_fixture="user")
def i_am_a_user_type_user(user_type):
    if user_type == "anonymous":
        return None
    if user_type == "staff":
        return UserFactory(is_staff=True, is_superuser=False)
    if user_type == "superuser":
        return UserFactory(is_staff=True, is_superuser=True)
    return UserFactory(is_staff=False, is_superuser=False)


@given(parsers.parse("I am logging in."), target_fixture="client")
def i_am_logging_in(user):
    client: APIClient = APIClient()
    if user:
        client.force_authenticate(user=user)
    return client


@when(parsers.parse("I am making a request to the server using the {method} and {path}."), target_fixture="response")
def i_am_making_a_request_to_the_server_using_the_method_and_path(client, method, path):
    response = None
    if method in ["GET", "get"]:
        response = client.get(path=path)
    if method in ["POST", "post"]:
        response = client.post(path=path)
    if method in ["PUT", "put"]:
        response = client.put(path=path)
    if method in ["PATCH", "patch"]:
        response = client.patch(path=path)
    if method in ["DELETE", "delete"]:
        response = client.delete(path=path)
    return response


@given(
    parsers.parse("The data to be sent is as follows.\n{payload}"),
    target_fixture="data",
)
def the_data_to_be_sent_is_as_follows(payload):
    return json.loads(payload)


@when(
    parsers.parse("I am making a request to the server with data using the {method} and {path}."),
    target_fixture="response",
)
def i_am_making_a_request_to_the_server_with_data_using_the_method_and_path(client, method, path, data):
    response = None
    if method in ["GET", "get"]:
        response = client.get(path=path, data=data)
    if method in ["POST", "post"]:
        response = client.post(path=path, data=data)
    if method in ["PUT", "put"]:
        response = client.put(path=path, data=data)
    if method in ["PATCH", "patch"]:
        response = client.patch(path=path, data=data)
    if method in ["DELETE", "delete"]:
        response = client.delete(path=path, data=data)
    return response


@given(
    parsers.parse("I will save the following data using {module}'s {factory_class_name}.\n{data}"),
)
def i_will_save_the_following_data_using_modules_factory_class_name(module: str, factory_class_name: str, data):
    module = importlib.import_module(module)
    factory_class = getattr(module, factory_class_name)
    factory_class(**json.loads(data))
    return None


@then(parsers.parse("The response status code is {status_code:d}."))
def the_response_status_code_is_status_code(response, status_code):
    assert response.status_code == status_code


@then(parsers.parse("The number of result in the response JSON is {number:d}."))
def the_number_of_result_in_the_response_json_is_number(response, number):
    assert len(response.json()) == number


@then(parsers.parse("The {field} data in the response JSON is the same as {value}."))
def the_field_data_in_the_response_json_is_the_same_as_value(response, field, value):
    assert str(response.json()[field]) == value


@then(parsers.parse("The {field} data in the response JSON is of type {data_type} and the same as {value}."))
def the_field_data_in_the_response_json_is_of_type_data_type_and_is_the_same_as_value(
    response, field, data_type, value
):
    data = response.json()[field]
    assert isinstance(data, DATA_TYPES.get(data_type, str)) is True
    assert str(data) == value


@then(
    parsers.parse(
        "The {field} data in the {index:d}st/nd/rd/th entry of the response JSON list is the same as {value}."
    )
)
def the_field_data_in_the_indexstndrdth_entry_of_the_response_json_list_is_the_same_as_value(
    response, field, index, value
):
    assert str(response.json()[int(index) - 1][field]) == value


@then(
    parsers.parse(
        "The {field} data in the {index:d}st/nd/rd/th entry of the response JSON list is of type {data_type} and the same as {value}."
    )
)
def the_field_data_in_the_indexstndrdth_entry_of_the_response_json_results_list_is_of_type_data_type_and_the_same_as_value(
    response, field, index, value
):
    assert str(response.json()[int(index) - 1][field]) == value


@then(parsers.parse("The existence of data with an ID of {pk:d} in the {model} model from {module} is {existance}."))
def the_existence_of_data_with_an_id_of_pk_in_the_model_model_from_module_is_existance(pk, model, module, existance):
    module = importlib.import_module(module)
    model_class = getattr(module, model)
    obj = model_class.objects.filter(pk=pk).last()
    assert str(bool(obj)) == existance


@then(
    parsers.parse(
        "The {field} data of the {model} model from {module} with an ID of {pk:d} is of type {data_type} and the same as {value}."
    )
)
def the_field_data_of_the_model_model_from_module_with_an_id_of_pk_is_of_type_data_type_and_the_same_as_value(
    field, model, module, pk, data_type, value
):
    module = importlib.import_module(module)
    model_class = getattr(module, model)
    obj = model_class.objects.filter(pk=pk).last()
    attr = getattr(obj, field)
    assert bool(obj) is True
    assert isinstance(attr, DATA_TYPES.get(data_type, str)) is True
    assert str(attr) == value
