import datetime  # Import datetime module to work with date and time
import os  # Import the os module to work with the operating system, in particular to obtain environment variables
from requests import Response  # Import the Response class from the requests module to handle HTTP responses


class Logger:
    # Specifies the Logger class for logging HTTP requests and responses

    file_name = f"logs/log_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".log"

    # Create a file name for the log with the current date and time added for uniqueness

    @classmethod
    # The @classmethod decorator is used to determine the class method in Python
    # This means that the method belongs to the Logger class and not to an instance of this class
    def _write_log_to_file(cls, data: str):
        # def is a keyword to define a function or method
        # _write_log_to_file - method name. Starts with underlining, which usually means "internal" use in Python
        # cls is the first class method argument that refers to the Logger class itself
        # (data: str) - definition of the second argument, 'data', which should be a string (str)

        with open(cls.file_name, 'a', encoding='utf-8') as logger_file:
            # with is a keyword to create a context manager in Python that manages resources automatically
            # open() - function to open a file
            # cls.file_name is a class attribute that contains the log file name
            # 'a' - file opening mode, 'append', which means adding data to file end.
            # encoding='utf-8' - setting of file encoding in UTF-8, which allows to save text correctly including non-ASCII characters
            # as logger_file - create a logger_file variable that references an open file

            logger_file.write(data)
            # logger_file.write is a method of writing an object (logger_file)
            # This method is used to write a string (data) to a file
            # data - a string passed to the method containing data to write to the log file

    @classmethod
    def add_request(cls, url: str, data: dict, headers: dict, cookies: dict, method: str):
        # Method for adding HTTP query information to log.
        # url: query URL.
        # data: query data.
        # headers: request headers.
        # cookies: cookies request.
        # method: query method (GET, POST, etc.).

        testname = os.environ.get('PYTEST_CURRENT_TEST')
        # Retrieve the name of the current test from environment variables (if the test is run through pytest)

        data_to_add = f"\n-----\n"  # Start an entry for a new query
        data_to_add += f"Test: {testname}\n"  # Add Test Name
        data_to_add += f"Time: {str(datetime.datetime.now())}\n"  # Add Current Time
        data_to_add += f"Request method: {method}\n"  # Add HTTP Query Method
        data_to_add += f"Request URL: {url}\n"  # Add HTTP Request URL
        data_to_add += f"Request data: {data}\n"  # Add HTTP Query Data
        data_to_add += f"Request headers: {headers}\n"  # Add HTTP request headers
        data_to_add += f"Request cookies: {cookies}\n"  # Add a HTTP Query Cookie
        data_to_add += "\n"  # Adding an empty row to separate records

        cls._write_log_to_file(data_to_add)  # Call the method of writing data to the log file

    @classmethod
    def add_response(cls, response: Response):
        # Method for adding HTTP response information to log
        # response: HTTP request Response object

        cookies_as_dict = dict(response.cookies)
        # Converting HTTP Response Cooks to Dictionary

        headers_as_dict = dict(response.headers)
        # Convert HTTP response headers to dictionary

        data_to_add = f"Response code: {response.status_code}\n"  # Add HTTP Response Status Code
        data_to_add += f"Response text: {response.text}\n"  # Add HTTP Response Text
        data_to_add += f"Response headers: {headers_as_dict}\n"  # Add HTTP Response Headers
        data_to_add += f"Response cookies: {cookies_as_dict}\n"  # Adding an HTTP Cookie
        data_to_add += "\n-----\n"  # Add a separator to end the record

        cls._write_log_to_file(data_to_add)  # Call the method of writing data to the log file
