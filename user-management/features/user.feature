Feature: User management

  Scenario: Create a new user
    Given I have the user data
    When I send a POST request to "/users/signup"
    Then I receive a 201 response
    And the response contains the user data

  Scenario: Login an existing user
    Given I have an existing user's credentials
    When I send a POST request to "/token/"
    Then I receive a 200 response
    And the response contains an access token

  Scenario: Get user details
    Given I am logged in as a user
    When I send a GET request to "/"
    Then I receive a 200 response
    And the response contains the user data


  Scenario: Update username
    Given I am logged in as a user
    And I have the new username
    When I send a PUT request to "/user/update_username"
    Then I receive a 200 response
    And the response confirms the username is updated

  Scenario: Update password
    Given I am logged in as a user
    And I have the new password
    When I send a PUT request to "/user/update_password"
    Then I receive a 200 response
    And the response confirms the password is updated

  Scenario: Update email
    Given I am logged in as a user
    And I have the new email
    When I send a PUT request to "/user/update_email"
    Then I receive a 200 response
    And the response confirms the email is updated

  Scenario: Delete a user
    Given I have the user credentials for deletion
    When I send a PUT request to "/user/delete_user"
    Then I receive a 200 response
    And the response confirms the user is deleted
