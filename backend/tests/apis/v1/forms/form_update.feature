@django_db
Feature: Form Update Test
  Background:
    Given I will save the following data using backend.tests.apis.factories's FormFactory.
          """
          {
            "id": 1,
            "slug": "test",
            "title": "test",
            "start_date": "2023-12-01",
            "end_date": "2023-12-31"
          }
          """
    And The data to be sent is as follows.
        """
        {
          "title": "test1"
        }
        """

  Scenario Outline: Form Partial Update Permission Test
    Given I am a/an <user_type> user.
    And I am logging in.
    When I am making a request to the server with data using the PATCH and /v1/forms/test/.
    Then The response status code is <status_code>.
  Examples:
    | user_type | status_code |
    | anonymous | 403 |
    | general | 403 |
    | staff | 200 |


  Scenario: Form Partial Update Test
    Given I am a/an staff user.
    And I am logging in.
    When I am making a request to the server with data using the PATCH and /v1/forms/test/.
    Then The response status code is 200.
    And The id data in the response JSON is the same as 1.
    And The title data in the response JSON is the same as test1.
    And The existence of data with an ID of 1 in the Form model from apps.forms.models is True.
    And The title data of the Form model from apps.forms.models with an ID of 1 is of type str and the same as test1.
