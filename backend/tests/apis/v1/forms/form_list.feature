@django_db
Feature: Form List Test
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

  Scenario Outline: Form List Permission Test
    Given I am a/an <user_type> user.
    And I am logging in.
    When I am making a request to the server using the GET and /v1/forms/.
    Then The response status code is <status_code>.
  Examples:
    | user_type | status_code |
    | anonymous | 200 |
    | general | 200 |
    | staff | 200 |

  Scenario: Form List Test
    Given I am a/an general user.
    And I am logging in.
    When I am making a request to the server using the GET and /v1/forms/.
    Then The response status code is 200.
    And The number of result in the response JSON is 1.
    And The slug data in the 1st/nd/rd/th entry of the response JSON list is the same as test.
    And The title data in the 1st/nd/rd/th entry of the response JSON list is of type str and the same as test.
