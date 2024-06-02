from behave import *
from fastapi.testclient import TestClient
from app.main import app
from app.db import db_dependency


client = TestClient(app)


@given("I have a new user data")
def step_impl(context):
    context.user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword",
    }


@when('I send a POST request to "/signup"')
def step_impl(context):
    context.response = client.post("user/signup", json=context.user_data)


@then("I receive a 201 response")
def step_impl(context):
    assert context.response.status_code == 201


@then("the response contains the user data")
def step_impl(context):
    response_data = context.response.json()
    assert response_data["username"] == context.user_data["username"]


@given("I have an existing user's credentials")
def step_impl(context):
    context.login_data = {"username": "newuser", "password": "newpassword"}


@when('I send a POST request to "/token/"')
def step_impl(context):
    context.response = client.post("user/token/", data=context.login_data)


@then("I receive a 200 response")
def step_impl(context):
    assert context.response.status_code == 200


@then("the response contains an access token")
def step_impl(context):
    response_data = context.response.json()
    assert "access_token" in response_data


@given("I am logged in as a user")
def step_impl(context):
    login_response = client.post("user/token/", data=context.login_data)
    context.token = login_response.json()["access_token"]


@when('I send a GET request to "user/"')
def step_impl(context):
    headers = {"Authorization": f"Bearer {context.token}"}
    context.response = client.get("user/", headers=headers)


@then("the response contains the user data")
def step_impl(context):
    response_data = context.response.json()
    assert "User" in response_data
    assert response_data["User"]["username"] == context.login_data["username"]


@when('I send a PUT request to "/user/update_username"')
def step_impl(context):
    global access_token
    response = client.post(
        "/user/update_username",
        json=context.new_username,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    context.response = response


@then("the response confirms the username is updated")
def step_impl(context):
    response_data = context.response.json()
    assert response_data["message"] == "Username updated successfully"


@when('I send a PUT request to "/user/update_password"')
def step_impl(context):
    global access_token
    response = client.put(
        "/user/update_password",
        json=context.new_password,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    context.response = response


@then("the response confirms the password is updated")
def step_impl(context):
    response_data = context.response.json()
    assert response_data["message"] == "Password updated successfull"


@when('I send a PUT request to "/user/update_email"')
def step_impl(context):
    global access_token
    response = client.post(
        "/user/update_email",
        json=context.new_email,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    context.response = response


@then("the response confirms the email is updated")
def step_impl(context):
    response_data = context.response.json()
    assert response_data["message"] == "Email updated successfully"


@when('I send a POST request to "/user/delete_user"')
def step_impl(context):
    response = client.post("/user/delete_user", json=context.user_data)
    context.response = response


@then("the response confirms the user is deleted")
def step_impl(context):
    response_data = context.response.json()
    assert response_data["message"] == "User deleted successfully"
