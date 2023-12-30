@django_db
Feature: Form Delete Test
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

  Scenario Outline: Form Delete Permission Test
    Given I am a/an <user_type> user.
    And I am logging in.
    When I am making a request to the server using the DELETE and /v1/forms/test/.
    Then The response status code is <status_code>.
  Examples:
    | user_type | status_code |
    | anonymous | 403 |
    | general | 403 |
    | staff | 204 |

  Scenario: Form Delete Test
    Given I am a/an staff user.
    And I am logging in.
    When I am making a request to the server using the DELETE and /v1/forms/test/.
    Then The response status code is 204.
    And The existence of data with an ID of 1 in the Form model from apps.forms.models is False.