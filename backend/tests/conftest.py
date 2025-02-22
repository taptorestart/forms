import importlib
import json
from types import NoneType

import pytest
from django.contrib.auth.models import User
from pytest_bdd import given, parsers, when, then
from rest_framework.test import APIClient

from tests.factories import UserFactory


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


def get_nested_value(data, key_path):
    keys = key_path.split(":")
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data


@given(parsers.parse("I am a {user_type} user."), target_fixture="user")
def i_am_a_user_type_user(user_type):
    if user_type == "anonymous":
        return None
    if user_type == "staff":
        return UserFactory(is_staff=True, is_superuser=False)
    if user_type == "superuser":
        return UserFactory(is_staff=True, is_superuser=True)
    return UserFactory(is_staff=False, is_superuser=False)


@given(parsers.parse("I am logged in."), target_fixture="client")
def i_am_logged_in(user):
    client: APIClient = APIClient()
    if user:
        client.force_authenticate(user=user)
    return client


@when(parsers.parse("I am making a {method} request to {path}."), target_fixture="response")
def i_am_making_a_method_request_to_path(client, method, path):
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


@given(parsers.parse("The following data will be sent:"), target_fixture="data")
def the_following_data_will_be_sent(docstring):
    return json.loads(docstring)


@when(
    parsers.parse("I am sending a {method} request to {path} with data."),
    target_fixture="response",
)
def i_am_sending_a_method_request_to_path_with_data(client, method, path, data):
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
    parsers.cfparse("I will save the following data using {model_class_name} model:"),
)
def i_will_save_the_following_data_using_factory_class_name_from_module(model_class_name: str, docstring):
    module = importlib.import_module("backend.tests.factories")
    factory_class_name = f"{model_class_name}Factory"
    factory_class = getattr(module, factory_class_name)
    factory_class(**json.loads(docstring))
    return None


@then(parsers.parse("The response status code is {status_code:d}."))
def the_response_status_code_is_status_code(response, status_code):
    assert response.status_code == status_code


@then("The response JSON should equal:")
def the_response_json_should_equal(response, docstring):
    expected_json = json.loads(docstring)
    actual_json = response.json()

    assert actual_json == expected_json


@then("The response JSON should contain the following key-value pairs:")
def the_response_json_should_equal(response, docstring):
    expected_json = json.loads(docstring)
    actual_json = response.json()

    for key, value in expected_json.items():
        assert key in actual_json
        assert actual_json[key] == value


@then(parsers.parse("The number of results in the response JSON is {number:d}."))
def the_number_of_results_in_the_response_json_is_number(response, number):
    assert len(response.json()) == number


@then(parsers.parse("The {field} data in the response JSON is the same as {value}."))
def the_field_data_in_the_response_json_is_the_same_as_value(response, field, value):
    assert str(get_nested_value(response.json(), field)) == value


@then(parsers.parse("The {field} data in the response JSON is of type {data_type} and the same as {value}."))
def the_field_data_in_the_response_json_is_of_type_data_type_and_is_the_same_as_value(
    response, field, data_type, value
):
    data = response.json()[field]
    assert isinstance(data, DATA_TYPES.get(data_type, str)) is True
    assert str(data) == value


@then(parsers.parse("The {field} data in the {index:d}th entry of the response JSON list is the same as {value}."))
def the_field_data_in_the_index_th_entry_of_the_response_json_list_is_the_same_as_value(response, field, index, value):
    data = get_nested_value(response.json()[index - 1], field)
    assert str(data) == value


@then(
    parsers.parse(
        "The {field} data in the {index:d}th entry of the response JSON list is of type {data_type} and the same as {value}."
    )
)
def the_field_data_in_the_index_th_entry_of_the_response_json_results_list_is_of_type_data_type_and_the_same_as_value(
    response, field, index, value
):
    data = get_nested_value(response.json()[index - 1], field)
    assert str(data) == value


@then(parsers.parse("It is {existance} that a record with an ID of {pk:d} exists in the {model} model from {module}."))
def it_is_existance_that_a_record_with_an_id_of_pk_exists_in_the_model_model_from_module(pk, model, module, existance):
    module = importlib.import_module(module)
    model_class = getattr(module, model)
    obj = model_class.objects.filter(pk=pk).last()
    assert str(bool(obj)) == existance


@then(
    parsers.parse(
        "The {field} field of the {model} model from {module} with an ID of {pk:d} is of type {data_type} and equals {value}."
    )
)
def the_field_field_of_the_model_model_from_module_with_an_id_of_pk_is_of_type_data_type_and_equals_value(
    field, model, module, pk, data_type, value
):
    module = importlib.import_module(module)
    model_class = getattr(module, model)
    obj = model_class.objects.filter(pk=pk).last()
    attr = getattr(obj, field)
    assert bool(obj) is True
    assert isinstance(attr, DATA_TYPES.get(data_type, str)) is True
    assert str(attr) == value
