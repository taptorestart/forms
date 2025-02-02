@django_db
Feature: Form Create Test
  Scenario Outline: Form Create Permission Test
    Given I am a <user_type> user.
    And I am logged in.
    And The following data will be sent.
        """
        {
          "slug": "test",
          "title": "test",
          "start_date": "2023-12-01",
          "end_date": "2023-12-31"
        }
        """
    When I am sending a POST request to /v1/forms/ with data.
    Then The response status code is <status_code>.
  Examples:
    | user_type | status_code |
    | anonymous | 403 |
    | general | 403 |
    | staff | 201 |

  Scenario: Form Create Test
    Given I am a staff user.
    And I am logged in.
    And The following data will be sent.
        """
        {
          "slug": "test",
          "title": "test",
          "start_date": "2023-12-01",
          "end_date": "2023-12-31"
        }
        """
    When I am sending a POST request to /v1/forms/ with data.
    Then The response status code is 201.
    And The slug data in the response JSON is the same as test.
    And The title data in the response JSON is of type str and the same as test.
