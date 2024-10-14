Feature: Customer Registration, Login

  Scenario: Successfully register a new customer
    Given the customer registration endpoint "v1/customer/register" is available
    When a customer submits a POST request to "v1/customer/register" with valid registration details:
      | username | email           | password   |
      | johndoe  | john@example.com| securePass123* |
    Then the response status code should be 201
    And the response should contain a success message with
    | field       | value            |
    | email       | test@example.com |
    | username    | testuser         |
    | customer_id | 123              |
    And the customer should be stored in the database

  @skip
  Scenario: Attempt to register with an existing username
    Given a customer with username "existinguser" is already registered
    When a customer submits a POST request to "v1/customer/register" with:
      | username    | email           | password   |
      | existinguser| new@example.com | newPass123 |
    Then the response status code should be 400
    And the response should contain an error message about duplicate username

  Scenario: Successfully login a registered customer
    Given a registered customer with credentials:
      | email | password   |
      | new@example.com  | securePass123 |
    When the customer submits a POST request to "v1/customer/login" with valid credentials
    Then the response status code should be 200
    And the response should contain an authentication token

  @skip
  Scenario: Attempt to login with invalid credentials
    When a customer submits a POST request to "v1/customer/login" with invalid credentials:
      | username | password   |
      | johndoe  | wrongpass  |
    Then the response status code should be 401
    And the response should contain an error message about invalid credentials
