import os  # Import os module to work with environment variables


class Environment:
    # Defining Environment Class for Environment Configuration Management

    DEV = 'dev'  # Constant for the test (dev) environment
    PROD = 'prod'  # Constant for product (prod) environment

    URLS = {
        DEV: 'https://playground.learnqa.ru/api_dev',
        PROD: 'https://playground.learnqa.ru/api'
    }

    # URLS dictionary containing basic URLs for different environments

    def __init__(self):
        # Environment class constructor

        # Setting ENV variable that is equal to 'prod'
        # os.environ['ENV'] = 'dev'
        # If you uncomment this string, the ENV environment variable will be set to 'dev'

        # Retrieve the ENV environment variable using the os.environ.get method.
        # If ENV is not installed, the default value is DEV ('dev')
        self.env = os.environ.get('ENV', self.DEV)

        try:
            # Attempt to get the value of ENV environment variable
            self.env = os.environ['ENV']
        except KeyError:
            # If the ENV variable is not defined, it will give a KeyError exception.
            # In this case, the default value is set to DEV ('dev')
            self.ENV = self.DEV

    def get_base_url(self):
        # Method to obtain the base URL depending on the current environment

        if self.env in self.URLS:
            # Check if the current environment is in the URLS dictionary
            return self.URLS[self.env]
            # Return the appropriate URL for the current environment
        else:
            # If the current environment is not found in the URLS dictionary, an exception is issued
            raise Exception(f"Unknown value of ENV variable {self.env}")


ENV_OBJECT = Environment()
# Create an instance of the Environment class

# print(os.getenv('ENV'))
# Edited call of print to output ENV environment variable value

# print(ENV_OBJECT.get_base_url())
# Edited call of print to output base URL of current environment
