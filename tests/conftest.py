# Defines the pytest_configure function, which is part of the pytest system
# This function is called to configure pytest before starting tests
def pytest_configure(config):
    # config: pytest configuration object that provides access to settings and test parameters

    # Add a new "flaky" marker to the pytest configuration.
    # This marker allows you to mark tests that should be restarted if they fail
        config.addinivalue_line(
        # The addinivalue_line method is used to add a string to the configuration file pytest.ini.
        "markers",
        # Specify adding a new marker

        "flaky: mark test to be retried up to 3 times with a 5 seconds delay"
        # Marker Description: tests with this marker will be restarted up to 3 times with a 5-second delay between attempts,
        # if they failed
    )
