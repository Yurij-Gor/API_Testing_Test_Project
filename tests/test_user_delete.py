from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("User Management")
@allure.feature("User Deletion")
class TestUserDelete(BaseCase):

    @allure.story("Attempt to delete a protected user")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.issue("DEL-1", "http://issue-tracker/DEL-1")
    @allure.description("Attempt to delete user with ID 2")
    def test_delete_user_by_id_2(self):
        # This test checks whether a protected user with a specific ID (ID=2) can be deleted

        # Generate data to authenticate a known user
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        # Send POST Authorization Request
        response_login = MyRequests.post("/user/login", data=login_data)
        # Verify that response status code is 200 (successful authorization)
        Assertions.assert_code_status(response_login, 200)

        # Get cookies and authorization token from server response
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")
        cookies = {"auth_sid": auth_sid}
        headers = {"x-csrf-token": token}
        # Trying to remove a user from ID 2 using cookies and authorization token
        response_delete = MyRequests.delete("/user/2", cookies=cookies, headers=headers)

        # Verify that the server returned an error and did not allow user deletion
        Assertions.assert_code_status(response_delete, 400)
        assert response_delete.text == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"User with ID 2 was deleted! This shouldn't have happened. Response text is {response_delete.text}"

        """
        Assertions.assert_json_value_by_name(
            response_delete, "error", "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            "User with ID 2 was deleted! This shouldn't have happened."
        )
        """

    @allure.story("Successful user deletion")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase("TC-2", "http://test-case/TC-2")
    @allure.description("Positive user deletion test")
    def test_delete_user_successfully(self):
        # This test verifies process of successful removing a user from the system (verifies user removal functionality
        # and that this remote user is no longer available on the system.)

        # Create data to register a new user
        register_data = self.prepare_registration_data()
        # Send POST request for registration
        response_register = MyRequests.post("/user/", data=register_data)
        # Verify successful response status code
        Assertions.assert_code_status(response_register, 200)
        # Extract user ID from server response
        user_id = self.get_json_value(response_register, "id")

        # Log in under a newly created user
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response_login = MyRequests.post("/user/login", data=login_data)
        Assertions.assert_code_status(response_login, 200)

        # Get cookies and authorization token from server response
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # Delete user using his ID and authorization cookies
        cookies = {"auth_sid": auth_sid}
        headers = {"x-csrf-token": token}
        response_delete = MyRequests.delete(f"/user/{user_id}", cookies=cookies, headers=headers)
        Assertions.assert_code_status(response_delete, 200)

        # Trying to retrieve the data of the remote user to verify that it has been deleted
        response_get = MyRequests.get(f"/user/{user_id}")
        # Verify that the user is actually deleted (pending status code 404 and corresponding message)
        Assertions.assert_code_status(response_get, 404)
        assert response_get.text == "User not found", \
            f"Error message is absent. Maybe user was not deleted. Response text is {response_get.text}"

        """
        Assertions.assert_json_value_by_name(
            response_get, "error", "User not found",
            "Error message is absent. Maybe user was not deleted"
        )
        """

    @allure.story("Attempt to delete a user by another user")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase("TC-23", "http://test-case/TC-23")
    @allure.description("Negative test for deleting a user by another user")
    def test_delete_user_by_another_user(self):
        # This test verifies the scenario when one user attempts to delete another user’s account,
        # which is an unacceptable security and policy action for most systems.

        # Register the first user
        user1_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=user1_data)
        Assertions.assert_code_status(response1, 200)
        user1_id = self.get_json_value(response1, "id")

        # Register the Second User
        user2_data = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=user2_data)
        Assertions.assert_code_status(response2, 200)

        # Log in as a second user
        login_data = {
            'email': user2_data['email'],
            'password': user2_data['password']
        }
        response_login = MyRequests.post("/user/login", data=login_data)
        Assertions.assert_code_status(response_login, 200)

        # Receive cookies and second user authorization token
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # Trying to delete the first user by authorizing under the second user
        cookies = {"auth_sid": auth_sid}
        headers = {"x-csrf-token": token}
        response_delete = MyRequests.delete(f"/user/{user1_id}", cookies=cookies, headers=headers)

        # Verify that the server did not allow deletion and returned an error
        Assertions.assert_code_status(response_delete, 400)
        assert response_delete.text == "You can delete only your account", \
            f"Error message is absent. Maybe user was deleted by another user. Response text is {response_delete.text}"

        """
        Assertions.assert_json_value_by_name(
            response_delete, "error", "You can delete only your account",
            "Error message is absent. Maybe user was deleted by another user."
        )
        """
