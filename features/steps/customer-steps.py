import requests
from behave import given, when, then
import json

# Base URL for your API
BASE_URL = "http://127.0.0.1:8000"  # Remove the trailing slash

@given('the customer registration endpoint "{endpoint}" is available')
def step_impl(context, endpoint):
    context.registration_endpoint = f"{BASE_URL}{endpoint}"
    print(f"Registration endpoint: {context.registration_endpoint}")

@when('a customer submits a POST request to {endpoint} with valid registration details')
def step_impl(context, endpoint):
    registration_data = {
        "username": "johndoe",
        "email": "john@example.com",
        "password": "securePass123*"
    }
    full_url =  f"{BASE_URL}/{endpoint.strip('\"')}"

    try:
        response = requests.post(full_url, json=registration_data)
        context.response = response  # Store the response in the context
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        context.response = None

@then('the response status code should be {status_code:d}')
def step_impl(context, status_code):
    assert context.response is not None, "No response was received"
    assert context.response.status_code == status_code, f"Expected status code {status_code}, but got {context.response.status_code}"


@then('the response should contain a success message with')
def step_impl(context):
    assert context.response is not None, "No response was received"
    response_data = context.response.json()

    for row in context.table:
        field = row['field']
        expected_value = row['value']
        assert field in response_data, f"{field} not found in response"
        if field == 'customer_id':
            assert response_data[field] == int(expected_value), f"Expected {field} to be {expected_value}, but got {response_data[field]}"
        else:
            assert response_data[field] == expected_value, f"Expected {field} to be {expected_value}, but got {response_data[field]}"

    print("Response contains the expected success message structure and values")

@then('the customer should be stored in the database')
def step_impl(context):
    raise NotImplementedError('STEP: Then the customer should be stored in the database')

from behave import given, when, then

@given('a customer with username "{username}" is already registered')
def step_impl(context, username):
    raise NotImplementedError('STEP: Given a customer with username "{username}" is already registered')

@when('a customer submits a POST request to "{endpoint}" with')
def step_impl(context, endpoint):
    raise NotImplementedError('STEP: When a customer submits a POST request to "{endpoint}" with')

@then('the response status code should be {status_code:d}')
def step_impl(context, status_code):
    raise NotImplementedError('STEP: Then the response status code should be {status_code:d}')

@then('the response should contain an error message about duplicate username')
def step_impl(context):
    raise NotImplementedError('STEP: Then the response should contain an error message about duplicate username')

@given('a registered customer with credentials')
def step_impl(context):
    # Store the credentials from the table in the context
    context.credentials = context.table[0].as_dict()
    print(f"Using credentials: {context.credentials}")

@when('the customer submits a POST request to "{endpoint}" with valid credentials')
def step_impl(context, endpoint):
    full_url = f"{BASE_URL}/{endpoint.strip('\"')}"
    print(f"Sending POST request to: {full_url}")

    try:
        response = requests.post(full_url, json=context.credentials)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        context.response = response
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        context.response = None

@then('the response status code should be {status_code:d}')
def step_impl(context, status_code):
    assert context.response is not None, "No response was received"
    assert context.response.status_code == status_code, \
        f"Expected status code {status_code}, but got {context.response.status_code}"

@then('the response should contain an authentication token')
def step_impl(context):
    assert context.response is not None, "No response was received"
    response_data = context.response.json()

    print(f"Response data: {response_data}")  # For debugging

    assert "access_token" in response_data, "access token not found in response"
    assert isinstance(response_data["access_token"], str), "Token should be a string"
    assert len(response_data["access_token"]) > 0, "Token should not be empty"

    # Optionally store the token for future use
    context.auth_token = response_data["access_token"]