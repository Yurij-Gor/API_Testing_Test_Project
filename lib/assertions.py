from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        """
        Verifies that the value with the specified name in JSON response matches the expected value.

        :param response: Object Response from the request containing JSON.
        :param name: Name of the key, which value should be checked in the JSON-response.
        :param expected_value: Expected value for comparison.
        :param error_message: Error message displayed in the case of value mismatch.

        An example of use:
        Assertions.assert_json_value_by_name(response, "user_id", 123, "User ID does not match the expected value.")
        """
        try:
            # Trying to convert the response body into a dictionary
            response_as_dict = response.json()
        except json.JSONDecodeError:
            # In case of error during convertion, display a message and complete the test
            assert False, f"Response is not in JSON format. Response text is {response.text}"

        # Verify that there is a key with specified name in the dictionary
        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

        # Compare the value on the specified key with the expected value
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            # Trying to convert response body into a dictionary
            response_as_dict = response.json()
        except json.JSONDecodeError:
            # In case of error during conversion, display a message and complete the test
            assert False, f"Response is not in JSON format. Response text is {response.text}"

        # Verify that the dictionary has a key with the specified name
        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            # Trying to convert response body into a dictionary
            response_as_dict = response.json()
        except json.JSONDecodeError:
            # In case of error during conversion, display a message and complete the test
            assert False, f"Response is not in JSON format. Response text is {response.text}"

        for name in names:
            # Verify that the dictionary has a key with the specified name
            assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            # Trying to convert response body into a dictionary
            response_as_dict = response.json()
        except json.JSONDecodeError:
            # In case of error during conversion, display a message and complete the test
            assert False, f"Response is not in JSON format. Response text is{response.text}"

        # Verify that the dictionary has a key with the specified name
        assert name not in response_as_dict, f"Response JSON shouldn't have key '{name}'. But it's present"

    @staticmethod
    def assert_json_has_not_keys(response: Response, names: list):
        # Create an empty list to store unexpected keys that have been discovered
        unexpected_keys = []
        try:
            # Trying to convert response body into a dictionary
            response_as_dict = response.json()
        except json.JSONDecodeError:
            # In case of error during conversion, display a message and complete the test
            assert False, f"Response is not in JSON format. Response text is {response.text}"

        # Iterate on all assigned key names
        for name in names:
            # Verify that the current key is present in the response
            if name in response_as_dict:
                # If a key is found, add it to the list of unexpected keys
                unexpected_keys.append(name)

            # Check if any unexpected keys have been found, and if so, drop an exception with information about these keys
            assert not unexpected_keys, f"Response shouldn't have keys {unexpected_keys}, but they are present"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        # Defining of a static method in a class. This method will be used to verify the status of the HTTP response.
        # Method parametrs:
        # response: the Response object received as a result of the HTTP request.
        # expected_status_code: expected response code status (such as 200, 404, etc.).

        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Expected: {expected_status_code}. Actual: {response.status_code}"
        # The assert statement is used to verify that the response code (response.status_code) status is equal to
        # expected status (expected_status_code). If this is not the case, the test will fail and cause an exception.
        # An error message that will be displayed if the expected code status and the actual code status do not match.
        # Message contains information about expected and actual code status for easy debugging.









