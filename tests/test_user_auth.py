import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Authorization")
@allure.feature("User Authentication")
class TestUserAuth(BaseCase):
    exclude_params = [
        "no_cookie",
        "no_token"
    ]

    def setup_method(self):
        # Method to configure the environment before running tests
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)

        # Extracting Data from Authentication Response
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")


    @allure.story("Successful authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.issue("AUTH-1", "http://issue-tracker/AUTH-1")
    @allure.testcase("TC-1", "http://test-case/TC-1")
    @allure.description("This test successfully autorize user by email and password")
    def test_auth_user(self):
        # User authentication validation test
        response2 = MyRequests.get(
            "/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
        )

        # Check with Assertions that user_id from authentication method matches user_id from verification method
        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            "User_id from auth method is not equal to user id from check method"
        )

    # Parameterizing to run a test with different conditions
    @allure.story("Authentication with missing credentials")
    @allure.severity(allure.severity_level.MINOR)
    @allure.testcase("TC-33", "http://test-case/TC-33")
    @allure.description("This test checks authorization status without sending auth cookie or token")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_check(self, condition):
        # Tests with different conditions to test negative scenarios

        if condition == "no_cookie":
            # Check that if there is no cookie "auth_sid" the user_id = 0 returns
            response2 = MyRequests.get(
                "/user/auth",
                headers={"x-csrf-token": self.token}
            )

        else:
            # Check that if there is no token in the request, user_id = 0 is returned
            response2 = MyRequests.get(
                "/user/auth",
                headers={"auth_sid": self.auth_sid}
            )

        # Checking with Assertions that user_id is 0 under a negative scenario
        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )
