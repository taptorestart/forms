@django_db
Feature: Form Create Test
  Background:
    Given The data to be sent is as follows.
        """
        {
          "slug": "test",
          "title": "test",
          "start_date": "2023-12-01",
          "end_date": "2023-12-31"
        }
        """

  Scenario Outline: Form Create Permission Test
    Given I am a/an <user_type> user.
    And I am logging in.
    When I am making a request to the server with data using the POST and /v1/forms/.
    Then The response status code is <status_code>.
  Examples:
    | user_type | status_code |
    | anonymous | 403 |
    | general | 403 |
    | staff | 201 |

  Scenario: Form Create Test
    Given I am a/an staff user.
    And I am logging in.
    When I am making a request to the server with data using the POST and /v1/forms/.
    Then The response status code is 201.
    And The slug data in the response JSON is the same as test.
    And The title data in the response JSON is of type str and the same as test.
