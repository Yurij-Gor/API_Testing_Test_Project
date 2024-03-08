import allure
import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("User Profile")
@allure.feature("User Data Retrieval")
class TestUserGet(BaseCase):
    @allure.story("Unauthorized user data retrieval")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase("TC-31", "http://test-case/TC-31")
    def test_get_user_details_not_auth(self):
        # Test checks that an unauthorized request can only get limited user data
        # (username only).
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")  # Check that "username" key is in the answer
        Assertions.assert_json_has_not_key(response, "email")  # Check that "email" key is missing
        Assertions.assert_json_has_not_key(response, "firstName")  # Check that "firstName" key is missing
        Assertions.assert_json_has_not_key(response, "lastName")  # Check that "lastName" key is missing

    @allure.story("Authorized user data retrieval")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase("TC-21", "http://test-case/TC-21")
    @pytest.mark.flaky(reruns=3, reruns_delay=5)
    def test_get_user_details_auth_as_same_user(self):
        # Test checks that an authorized user can get full information about himself
        # (username, email, first name, last name).
        data = {'email': 'vinkotov@example.com', 'password': '1234'}
        response1 = MyRequests.post("/user/login", data=data)  # User Authorization
        auth_sid = self.get_cookie(response1, "auth_sid")  # Getting the "auth_sid" cookie from the response
        token = self.get_header(response1, "x-csrf-token")  # Getting a token from the reply header
        user_id_from_auth_method = self.get_json_value(response1, "user_id")  # Getting a user’s ID from a response

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},  # Transfer token in header
            cookies={"auth_sid": auth_sid}  # Transfer cookies "auth_sid"
        )
        # Check the presence of keys "username", "email", "firstName", "lastName" in the answer
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)


@allure.epic("User Profile")
@allure.feature("User Data Retrieval")
class TestUserGetAnotherUser(BaseCase):
    @allure.story("Get Another User Details")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.issue("AUTH-11", "http://issue-tracker/AUTH-11")
    @allure.testcase("TC-11", "http://test-case/TC-11")
    def test_get_another_user_details(self):
        # The test is aimed at checking the security and privacy of user data on the system,
        # Making sure that the user cannot access the sensitive information of other users.
        # By using the first user’s token and cookies, the test requests the second user’s data.
        # The Test checks which data about another user can be obtained by being authorized under another account.

        # Step 1: Register the first user
        first_user_data = self.prepare_registration_data()  # Generate data for the first user
        response_first_user_register = MyRequests.post("/user/",
                                                       data=first_user_data)  # The First User Registration
        Assertions.assert_code_status(response_first_user_register, 200)  # Validate Successful Status Code

        # Step 2: Register the Second User
        second_user_data = self.prepare_registration_data()  # Data generation for the second user
        response_second_user_register = MyRequests.post("/user/",
                                                        data=second_user_data)  # Register the Second User
        Assertions.assert_code_status(response_second_user_register, 200)  # Validate Successful Status Code

        # Step 3: Extract ID and the second username
        second_user_id = self.get_json_value(response_second_user_register, "id")  # The Second User ID extraction
        second_user_username = second_user_data["username"]  # Extracting the second user username

        # Step 4: Log in under the first user
        login_data = {
            'email': first_user_data['email'],
            'password': first_user_data['password']
        }
        response_login = MyRequests.post("/user/login", data=login_data)  # The First User Authorization
        Assertions.assert_code_status(response_login, 200)  # Validate Successful Status Code

        # Extract data for authorization (auth_sid and token)
        auth_sid = self.get_cookie(response_login, "auth_sid")  # Extracting Cookies auth_sid
        token = self.get_header(response_login, "x-csrf-token")  # Extracting the Header Value x-csrf-token

        # Step 5: Query the second user’s id using token and auth_sid first
        # user
        response_get_another_user = MyRequests.get(
            f"/user/{second_user_id}",  # Querying the second user’s ID
            headers={"x-csrf-token": token},  # The First User Token Transfer in Request Header
            cookies={"auth_sid": auth_sid}  # Transfer cookies auth_sid first user
        )

        # Step 6: Check that only username (username) data is received
        expected_fields = ["username"]  # Expected fields in response
        Assertions.assert_json_has_keys(response_get_another_user, expected_fields)  # Check for expected fields

        # Check if there are no unexplained fields
        # Unexpected fields in the answer
        unexpected_fields = ["id", "email", "firstName", "lastName", "password", "token", "session_id", "auth_sid"]
        Assertions.assert_json_has_not_keys(response_get_another_user, unexpected_fields)

        # Verify that the 'username' field value matches the expected value (second user username)
        Assertions.assert_json_value_by_name(
            response_get_another_user, "username", second_user_username,
            "Unexpected username value for another user"
        )  # Check if the 'username' field matches the expected value
