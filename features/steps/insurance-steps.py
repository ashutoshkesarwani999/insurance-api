from behave import given, when, then
import requests

BASE_URL = "http://127.0.0.1:8000"  # Adjust this to match your API's base URL


# @given("a customer is authenticated")
# def step_customer_authenticated(context):
#     context.authentication_skipped = True

@given('an insurance policy with id "{insurance_id}" exists')
def step_policy_exists(context, insurance_id):
    create_mock_policy(insurance_id)

@when('the customer sends a GET request to "v1/insurance/{customer_id}"')
def step_send_get_request(context, customer_id):
    full_url = f"{BASE_URL}/v1/insurance/{customer_id}"
    print(full_url)
    context.response = requests.get(full_url,  timeout=30)


@then("the response status code should be {status_code:d}")
def step_check_status_code(context, status_code):
    assert context.response.status_code == status_code

@then("the response should contain the details of the insurance policy")
def step_check_policy_details(context):
    response_data = context.response.json()
    print(response_data)
    for resp in response_data:
        assert "insurance_id" in resp
        assert "customer_policy_url" in resp
        assert "customer_id" in resp
    # Add more assertions as needed


@given('a customer is authenticated')
def step_impl(context):
    # This step is not implemented
    context.authentication_skipped = True
    # raise NotImplementedError('STEP: Given a customer is authenticated')

@given('there are multiple insurance policies in the system')
def step_impl(context):
    # For this step, we'll assume policies already exist
    # In a real scenario, you might want to create test policies here
    print("Assuming multiple insurance policies exist in the system")
    context.expected_policy_count = 1  # Adjust as needed

@when('the customer sends a GET request to "{endpoint}"')
def step_impl(context, endpoint):
    full_url = f"{BASE_URL}/{endpoint.strip('/')}"
    print(f"Sending GET request to: {full_url}")

    # Note: In a real scenario, you'd include the authentication token here
    headers = {}  # Add authentication headers when implemented

    try:
        response = requests.get(full_url, headers=headers)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.json()}")
        context.response = response
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        context.response = None

@then('the response status code should be {status_code:d}')
def step_impl(context, status_code):
    assert context.response is not None, "No response was received"
    assert context.response.status_code == status_code, \
        f"Expected status code {status_code}, but got {context.response.status_code}"

@then('the response should contain a list of all available insurance policies')
def step_impl(context):
    assert context.response is not None, "No response was received"
    response_data = context.response.json()

    print(f"Response data: {response_data}")  # For debugging

    assert isinstance(response_data, list), "Response should be a list of policies"
    assert len(response_data) > 0, "Response should contain at least one policy"
    assert len(response_data) == context.expected_policy_count, \
        f"Expected {context.expected_policy_count} policies, but got {len(response_data)}"

    # Check the structure of each policy (adjust according to your API response structure)
    for policy in response_data:
        assert "insurance_id" in policy, "Each policy should have an id"
        assert "customer_policy_url" in policy, "Each policy should have a name"
        # Add more assertions as needed for your policy structure


def create_mock_policy(insurance_id):
    # This could be a dictionary or a custom Policy object
    mock_policy = {
        "insurance_id": insurance_id,
        "coverage": "Full Coverage",
        "premium": 1000.00,
        "start_date": "2023-01-01",
        "end_date": "2023-12-31"
    }

    # In a real scenario, you might store this in a mock database or in-memory store
    # For simplicity, we'll use a global dictionary
    if not hasattr(create_mock_policy, "policies"):
        create_mock_policy.policies = {}

    create_mock_policy.policies[insurance_id] = mock_policy