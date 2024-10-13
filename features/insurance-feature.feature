Feature: Fetch Insurance Policy details

  Scenario: Retrieve a specific insurance policy
    Given a customer is authenticated
    And an insurance policy with id "2" exists
    When the customer sends a GET request to "v1/insurance/2"
    Then the response status code should be 200
    And the response should contain the details of the insurance policy
  @skip
  Scenario: Attempt to retrieve a non-existent insurance policy
    Given a customer is authenticated
    When the customer sends a GET request to "v1/insurance/99999"
    Then the response status code should be 404
    And the response should contain an error message about policy not found

  Scenario: Retrieve all insurance policies
    Given a customer is authenticated
    And there are multiple insurance policies in the system
    When the customer sends a GET request to "v1/insurance/"
    Then the response status code should be 200
    And the response should contain a list of all available insurance policies

  @skip
  Scenario: Attempt to access insurance policies without authentication
    Given a customer is not authenticated
    When the customer sends a GET request to "v1/insurance/"
    Then the response status code should be 401
    And the response should contain an error message about unauthorized access
