import allure
import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("User Registration")
@allure.feature("User Signup Process")
class TestUserRegister(BaseCase):

    @allure.story("Successful user registration")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.issue("http://issue-tracker/REG-1", "REG-1")
    @allure.testcase("http://test-case/TC-4", "TC-4")
    @allure.description("Successful user creation")
    def test_user_create_successfully(self):
        """
        Test: Successful User Creation
        """
        data = self.prepare_registration_data()  # Data generation for registration

        response = MyRequests.post("/user/", data=data)  # Sending a POST request to create a user

        Assertions.assert_code_status(response, 200)  # Validate Successful Status Code
        Assertions.assert_json_has_key(response, "id")  # Check if the "id" key is in the JSON answer

    @allure.story("User registration with existing email")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase("http://test-case/TC-4", "TC-4")
    @allure.description("User registration with existing email")
    def test_creating_user_with_existing_email(self):
        # Test checks that you cannot create a user with email that already exists on the system

        email = 'vinkotov@example.com'  # Specify existing email
        data = self.prepare_registration_data(email)  # Preparing registration data with the specified email

        response = MyRequests.post("/user/", data=data)  # Send a POST request to create a new user

        # Check that the server’s response contains the status code 400, which means that the request failed
        Assertions.assert_code_status(response, 400)

        # Check that the text of server response corresponds to the expected: the user with such email already exists
        # If the response does not match the expectations, output an error message
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    @allure.story("User registration with invalid email")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase("http://test-case/TC-42", "TC-42")
    @allure.description("Сreating a user with an incorrect email (without the @ symbol)")
    def test_invalid_email(self):
        # Test: Create user with incorrect email (without @)

        data = self.prepare_registration_data(email='invalied_email')
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        expected_content = "Invalid email format"
        assert response.content.decode("utf-8") == expected_content, f"Unexpected response content {response.content}"

    @allure.story("User registration missing a field")
    @allure.severity(allure.severity_level.MINOR)
    @allure.testcase("http://test-case/TC-43", "TC-43")
    @allure.description("Creating a user without specifying one of the fields. Parameterized test to check the"
                        "absence of each of the fields")
    @pytest.mark.parametrize('missing_field', ['username', 'password', 'firstName', 'lastName', 'email'])
    def test_user_create_missing_field(self, missing_field):
        # Test: Create a user without specifying one of the fields
        # Parameterized test to check the absence of each field

        data = self.prepare_registration_data()  # Data generation for registration
        data.pop(missing_field)  # Remove one of the fields
        response = MyRequests.post("/user/", data=data)  # Sending a POST request to create a user
        Assertions.assert_code_status(response, 400)  # Check expected status code 400
        expected_content = f"The following required params are missed: {missing_field}"
        assert response.content.decode("utf-8") == expected_content, f"Unexpected response content {response.content}"

    @allure.story("User registration with too long username")
    @allure.severity(allure.severity_level.MINOR)
    @allure.testcase("http://test-case/TC-45", "TC-45")
    @allure.description("Сreating a user with a very short name of one character")
    def test_user_create_short_name(self):
        # Test: Create a user with a very short name in one character

        data = self.prepare_registration_data(username='a')  # Generate data with short name
        response = MyRequests.post("/user/", data=data)  # Sending a POST request to create a user
        Assertions.assert_code_status(response, 400)  # Check expected status code 400
        expected_content = "The value of 'username' field is too short"
        assert response.content.decode("utf-8") == expected_content, f"Unexpected response content {response.content}"

    @allure.story("User registration with too long username")
    @allure.severity(allure.severity_level.MINOR)
    @allure.testcase("http://test-case/TC-45", "TC-45")
    @allure.description("Creating a user with a very long name (longer than 250 characters)")
    def test_user_create_long_name(self):
        # Test: Create a user with a very long name (longer than 250 characters)

        long_name = 'a' * 251
        data = self.prepare_registration_data(username=long_name)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        expected_content = "The value of 'username' field is too long"
        assert response.content.decode("utf-8") == expected_content, f"Unexpected response content {response.content}"
