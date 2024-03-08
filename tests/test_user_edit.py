from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("User Profile")
@allure.feature("User Profile Editing")
class TestUserEdit(BaseCase):

    @allure.story("Edit profile after creating a new user")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.issue("http://issue-tracker/EDIT-1", "EDIT-1")
    @allure.testcase("http://test-case/TC-3", "TC-3")
    def test_edit_just_created_user(self):
        # Determine the test to edit the newly created user

        # Register a New User
        register_data = self.prepare_registration_data()  # Preparing Data for Registration
        response1 = MyRequests.post("/user", data=register_data)  # Send User Registration Request

        Assertions.assert_code_status(response1, 200)  # Check that the server response is 200 (successful)
        Assertions.assert_json_has_key(response1, "id")  # Check that the server response has the "id" key

        # Getting Data Used in Registration
        email = register_data['email']  # Getting Email
        password = register_data['password']  # Getting password
        user_id = self.get_json_value(response1, "id")  # Retrieve user ID from server response

        # Authorization under created user
        login_data = {
            'email': email,  # Using user e-mail
            'password': password  # Using a User Password
        }
        response2 = MyRequests.post("/user/login", data=login_data)  # Sending a User Authorization Request

        auth_sid = self.get_cookie(response2, "auth_sid")  # Getting auth_sid cookies from server response
        token = self.get_header(response2, "x-csrf-token")  # Getting x-csrf-token from server response

        # Editing User Data
        new_name = "Changed Name"  # New User Name

        # Sending a request to edit user data
        response3 = MyRequests.put(
            f"/user/{user_id}",  # URL for editing user data with his ID
            headers={"x-csrf-token": token},  # Transfer token in request header
            cookies={"auth_sid": auth_sid},  # Transfer cookies in query
            data={"firstName": new_name}  # Data to edit (new user name)
        )

        Assertions.assert_code_status(response3, 200)  # Check that the server response is 200 (successful)

        # Checking User Data Changes
        response4 = MyRequests.get(
            f"/user/{user_id}",  # URL to retrieve the user’s ID
            headers={"x-csrf-token": token},  # Transfer token in request header
            cookies={"auth_sid": auth_sid}  # Transfer cookies in query
        )

        # Verify that the username has been successfully changed
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",  # Key to be checked
            new_name,  # Expected value (new name)
            "Wrong name of the user after edit"
            # Error message if username does not match expected
        )


@allure.feature("User Profile Editing")
class TestUserEditNegative(BaseCase):
    @allure.story("Unauthorized user profile editing attempt")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase("http://test-case/TC-31", "TC-31")
    @allure.description("An attempt to edit user data without authorization")
    def test_edit_user_unauthorized(self):
        # Prepare test data
        user_id = 123  # Replace with a non-existent user identifier

        # Attempt to edit user data without authorization
        response = MyRequests.put(f"/user/{user_id}", data={"firstName": "NewName"})

        # Check that the response code is 400 (Bad Request)
        Assertions.assert_code_status(response, 400)
        assert response.json().get("error") == "Auth token not supplied",\
            f"Unexpected response content. Expected: Auth token not supplied, Actual: {response.text}"

        """
        Assertions.assert_json_value_by_name(
            response, "error", expected_content,
            f"Unexpected response content. Expected: {expected_content}, Actual: {response.text}")
        """

    @allure.story("Edit another user's profile")
    @allure.severity(allure.severity_level.MINOR)
    @allure.testcase("http://test-case/TC-32", "TC-32")
    @allure.description("Trying to edit another user's data")
    def test_edit_another_user_data(self):
        # Step 1: Register the first user
        first_user_data = self.prepare_registration_data()
        response_first_user_register = MyRequests.post("/user/",
                                                       data=first_user_data)  # First User Registration
        Assertions.assert_code_status(response_first_user_register, 200)

        # Step 3: Register the Second User
        second_user_data = self.prepare_registration_data()  # Data generation for the second user
        response_second_user_register = MyRequests.post("/user/",
                                                        data=second_user_data)  # Register a Second User
        Assertions.assert_code_status(response_second_user_register, 200)  # Validate successful Status Code

        # Extract the Second User ID
        second_user_id = self.get_json_value(response_second_user_register, "id")  # Extracting the Second User ID

        # Step 4: Log in under the first user
        login_data = {
            'email': first_user_data['email'],
            'password': first_user_data['password']
        }
        response_login_first_user = MyRequests.post("/user/login", data=login_data)  # The First User Authorization
        Assertions.assert_code_status(response_login_first_user, 200)  # Validate successful Status Code

        # Extract data for authorization (auth_sid and token)
        auth_sid_first_user = self.get_cookie(response_login_first_user,
                                              "auth_sid")  # Extracting Cookies auth_sid
        token_first_user = self.get_header(response_login_first_user,
                                           "x-csrf-token")  # Extracting the Header Value x-csrf-token

        # Attempt to edit the second user data as first user
        response = MyRequests.put(
            f"/user/{second_user_id}",
            headers={"x-csrf-token": token_first_user},
            cookies={"auth_sid": auth_sid_first_user},
            data={"firstName": "NewName"}
        )

        # Check that the response code is 403 (Forbidden)
        Assertions.assert_code_status(response, 403)

    @allure.story("Check server response when editing another user's profile")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase("http://test-case/TC-33", "TC-33")
    @allure.description("Checking the server response when trying to edit another user's data")
    def test_edit_another_user_data_check_response_text(self):
        # First User Registration
        # Generate data for the first user
        first_user_data = self.prepare_registration_data()
        # Send Request for the first user registration
        response_first_user_register = MyRequests.post("/user/", data=first_user_data)
        # Make sure the user is successfully registered (status code 200)
        Assertions.assert_code_status(response_first_user_register, 200)

        # First User Registration
        # Generate data for the first user
        second_user_data = self.prepare_registration_data()
        # Send the second user registration request
        response_second_user_register = MyRequests.post("/user/", data=second_user_data)
        # Make sure the user is successfully registered (status code 200)
        Assertions.assert_code_status(response_second_user_register, 200)
        # Get the ID of the second user from the server response
        second_user_id = self.get_json_value(response_second_user_register, "id")

        # First User Authorization
        # Generate login data (first user login and password)
        login_data = {'email': first_user_data['email'], 'password': first_user_data['password']}
        # Submit an authorization request
        response_login_first_user = MyRequests.post("/user/login", data=login_data)
        # Make sure that the authorization was successful (status code 200)
        Assertions.assert_code_status(response_login_first_user, 200)
        # Get cookies and authorization token from server response
        auth_sid_first_user = self.get_cookie(response_login_first_user, "auth_sid")
        token_first_user = self.get_header(response_login_first_user, "x-csrf-token")

        # Attempt to edit second user data by first user
        # Send a second user data change request
        response = MyRequests.put(
            f"/user/{second_user_id}",
            headers={"x-csrf-token": token_first_user},
            cookies={"auth_sid": auth_sid_first_user},
            data={"firstName": "NewName"}
        )

        # Check Server Response
        # Verify that the server response is as expected
        assert response.json().get("error") == "This user can only edit their own data.",\
            f"Unexpected response content. Expected: This user can only edit their own data, Actual: {response.text}"

        """
        Assertions.assert_json_value_by_name(
            response, "error", expected_content,
            f"Unexpected response content. Expected: {expected_content}, Actual: {response.text}")
        """

    @allure.story("Edit user email with invalid format")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase("http://test-case/TC-34", "TC-34")
    @allure.description("Attempt to edit user email with incorrect format")
    def test_edit_user_email_invalid_format(self):
        # User Registration
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)
        user_id = self.get_json_value(response, "id")

        # Authorization under registered user
        auth_data = {"email": register_data["email"], "password": register_data["password"]}
        auth_response = MyRequests.post("/user/login", data=auth_data)
        auth_sid = self.get_cookie(auth_response, "auth_sid")
        token = self.get_header(auth_response, "x-csrf-token")

        # Attempt to edit the wrong format user email
        response = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": "newemailwithoutat"}
        )

        # Check that the response code is 400 (Bad Request)
        Assertions.assert_code_status(response, 400)
        assert response.json().get("error") == "Invalid email format",\
            f"Unexpected response content. Expected: Invalid email format, Actual: {response.text}"

        """
        Assertions.assert_json_value_by_name(
            response, "error", expected_content,
            f"Unexpected response content. Expected: {expected_content}, Actual: {response.text}")
        """

    @allure.story("Edit user with too short firstName")
    @allure.severity(allure.severity_level.MINOR)
    @allure.testcase("http://test-case/TC-35", "TC-35")
    @allure.description("Trying to edit user's firstName with a very short value")
    def test_edit_user_firstName_short_value(self):
        # User Registration
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)
        user_id = self.get_json_value(response, "id")

        # Attempt to edit the user’s firstName with a very short value
        auth_data = {"email": register_data["email"], "password": register_data["password"]}
        auth_response = MyRequests.post("/user/login", data=auth_data)
        auth_sid = self.get_cookie(auth_response, "auth_sid")
        token = self.get_header(auth_response, "x-csrf-token")

        # Attempt to edit the user’s firstName with a very short value
        response = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": "A"}
        )

        # Check that the response code is 400 (Bad Request)
        Assertions.assert_code_status(response, 400)
        expected_content = "The value for field `firstName` is too short"
        Assertions.assert_json_value_by_name(
            response, "error", expected_content,
            f"Unexpected response content. Expected: {expected_content}, Actual: {response.text}")
