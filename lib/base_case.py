import json.decoder
from requests import Response
from datetime import datetime


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        """
        Method for extracting cookie value from the Response object.
        Verifies that cookies with specified name are present in response.
        If there are cookies, returns the value.
        """
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        """
        Method to extract a header value from the Response object.
        Verifies that the header with the specified name is present in the response.
        If there is a header, returns its value.
        """
        assert headers_name in response.headers, f"Cannot find header with name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        """
        This method is used to extract a value from the JSON response of the HTTP request.
        Trying to convert the response body into a dictionary.
        In the case of an error (for example, if the answer is not valid JSON),
        displays a message and completes the test.
        Verifies that the key with the specified name is present in the response dictionary.
        If there is a key, returns its value.
        """

        try:
            response_as_dict = response.json()  # Attempt to convert the JSON response into a Python dictionary.
        except json.decoder.JSONDecodeError:
            # This block of code will run if an error occurs during the conversion (for example, if the answer is not
            # is valid JSON).
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"
            # assert False will cause the test to fail.
            # The comma message will be shown as an explanation for the failure.

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        # This assert checks if the dictionary contains a key named 'name'.
        # If there is no key, the test is considered to be failed and the corresponding message is displayed.

        return response_as_dict[name]  # Returns the value corresponding to the 'name' key.

    def prepare_registration_data(self, email=None, password='123', username='learnqa', firstName='learnqa',
                                   lastName='learnqa'):
        """
        This method is designed to prepare data for user registration.
        Method parameters may be set explicitly or default values may be used.
        """
        if email is None:  # Verify if the email parameter is set. If not, we create the email ourselves
            base_part = "learnqa"  # Basic email part
            domain = "example.com"  # Domain for email
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            # Generate unique part of email using current date and time to avoid repetition

            email = f"{base_part}{random_part}@{domain}"
            # Generation of full email address by combining its parts

        return {
            'password': password,  # Return the specified password or use the default password
            'username': username,  # Return the specified username or use the default username
            'firstName': firstName,  # Return the specified firstName or use the default firstName
            'lastName': lastName,  # Return the specified lastName or use the default lastName
            'email': email  # Return the created email
        }
        # Method returns dictionary with data to register


"""
    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email =f{base_part}{random_part}@{domain}
            
        return {
            'password': '123'
            'username': 'learnqa'
            'firstName': 'learnqa'
            'lastName':  'learnqa'
            'email': email
        }
        
"""