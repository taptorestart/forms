@django_db
Feature: Form List Test
  Background:
    Given I will save the following data using FormFactory from backend.tests.apis.factories.
          """
          {
            "id": 1,
            "slug": "test",
            "title": "test",
            "start_date": "2023-12-01",
            "end_date": "2023-12-31"
          }
          """

  Scenario Outline: Form List Permission Test
    Given I am a <user_type> user.
    And I am logged in.
    When I am making a GET request to /v1/forms/.
    Then The response status code is <status_code>.
  Examples:
    | user_type | status_code |
    | anonymous | 200 |
    | general | 200 |
    | staff | 200 |

  Scenario: Form List Test
    Given I am a general user.
    And I am logged in.
    When I am making a GET request to /v1/forms/.
    Then The response status code is 200.
    And The number of results in the response JSON is 1.
    And The slug data in the 1th entry of the response JSON list is the same as test.
    And The title data in the 1th entry of the response JSON list is of type str and the same as test.
