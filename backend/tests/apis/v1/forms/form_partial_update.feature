@django_db
Feature: Form Partial Update Test
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

  Scenario Outline: Form Partial Update Permission Test
    Given I am a <user_type> user.
    And I am logged in.
    And The following data will be sent:
        """
        {
          "title": "test1"
        }
        """
    When I am sending a PATCH request to /v1/forms/test/ with data.
    Then The response status code is <status_code>.
  Examples:
    | user_type | status_code |
    | anonymous | 403 |
    | general | 403 |
    | staff | 200 |


  Scenario: Form Partial Update Test
    Given I am a staff user.
    And I am logged in.
    And The following data will be sent:
        """
        {
          "title": "test2"
        }
        """
    When I am sending a PATCH request to /v1/forms/test/ with data.
    Then The response status code is 200.
    And The response JSON should equal:
        """
        {
            "id": 101,
            "slug": "test",
            "start_date": "2023-12-01T00:00:00Z",
            "end_date": "2023-12-31T00:00:00Z",
            "title": "test2",
            "components": []
        }
        """
    And The response JSON should contain the following key-value pairs:
        """
        {
            "slug": "test",
            "title": "test2"
        }
        """
    And The id data in the response JSON is the same as 101.
    And The title data in the response JSON is the same as test2.
    And It is True that a record with an ID of 101 exists in the Form model from apps.forms.models.
    And The title field of the Form model from apps.forms.models with an ID of 101 is of type str and equals test2.
