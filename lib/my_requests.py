import requests  # Import requests module to send HTTP requests
from lib.logger import Logger  # Import Logger to log HTTP requests and responses
import allure  # Import allure module to work with Allure framework for testing
from environment import ENV_OBJECT  # Import ENV_OBJECT to access environment settings


class MyRequests:
    # Defining the MyRequests class for convenient sending of HTTP requests

    @staticmethod
    def post(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        # Define static method for sending POST requests
        # url: query URL
        # data: the data to send in the request (request body)
        # headers: request headers
        # cookies: cookies for request

        with allure.step(f"POSt request to url '{url}'"):
            # Creation a step in Allure report with description of sending POST-request

            return MyRequests._send(url, data, headers, cookies, "POST")
            # Calling private method _send to execute query

    @staticmethod
    def get(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        # Similar definition of the method for GET-requests

        with allure.step(f"GET request to URL '{url}'"):
            # Step in Allure report for GET-request

            return MyRequests._send(url, data, headers, cookies, "GET")
            # Call _send for GET-request

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        # Method for PUT-requests

        with allure.step(f"PUT request to URL '{url}'"):
            # Step in Allure report for PUT-request

            return MyRequests._send(url, data, headers, cookies, "PUT")
            # Call _send for PUT-request

    @staticmethod
    def delete(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        # Method for DELETE-requests

        with allure.step(f"DELETE request to URL '{url}'"):
            # Step in Allure report for DELETE-request

            return MyRequests._send(url, data, headers, cookies, "DELETE")
            # Call _send for DELETE-request

    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method: str):
        # Private method for sending a request.
        # method: type of HTTP method (GET, POST, PUT, DELETE)

        url = f"{ENV_OBJECT.get_base_url()}{url}"
        # Generating a full URL for request by adding a basic URL

        if headers is None:
            headers = {}
        # Initializing headers with an empty dictionary if no headers are sent

        if cookies is None:
            cookies = {}
        # Initializing cookies with an empty dictionary if no cookies are sent

        Logger.add_request(url, data, headers, cookies, method)
        # Logging information about request

        # Selecting request method depending on the method value and sending a request
        if method == 'GET':
            response = requests.get(url, params=data, headers=headers, cookies=cookies)
        elif method == 'POST':
            response = requests.post(url, params=data, headers=headers, cookies=cookies)
        elif method == 'PUT':
            response = requests.put(url, params=data, headers=headers, cookies=cookies)
        elif method == 'DELETE':
            response = requests.delete(url, params=data, headers=headers, cookies=cookies)
        else:
            # In  case  of incorrect method exception is caused
            raise Exception(f"Bad HTTP method {method} was received")

        Logger.add_response(response)
        # Logging received response

        return response
        # Return response object to calling code
