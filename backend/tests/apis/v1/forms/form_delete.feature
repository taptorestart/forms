@django_db
Feature: Form Delete Test
  Background:
    Given I will save the following data using Form model:
          """
          {
            "id": 101,
            "slug": "test",
            "title": "test",
            "start_date": "2023-12-01",
            "end_date": "2023-12-31"
          }
          """

  Scenario Outline: Form Delete Permission Test
    Given I am a <user_type> user.
    And I am logged in.
    When I am making a DELETE request to /v1/forms/test/.
    Then The response status code is <status_code>.
  Examples:
    | user_type | status_code |
    | anonymous | 403 |
    | general | 403 |
    | staff | 204 |

  Scenario: Form Delete Test
    Given I am a staff user.
    And I am logged in.
    When I am making a DELETE request to /v1/forms/test/.
    Then The response status code is 204.
    And It is False that a record with an ID of 101 exists in the Form model from apps.forms.models.