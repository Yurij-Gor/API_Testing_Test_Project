FROM python
# Basic Image: Official Python Image with Docker Hub. This means that the container will be built based on
# ready-made Python environment.

WORKDIR /tests_project/
# Installing a working directory inside the container. All following commands will be executed from this directory.

COPY requirements.txt .
# Copy the requirements.txt file from the local directory to the container’s working directory.
# The requirements.txt file contains a list of Python dependencies.

RUN pip install -r requirements.txt
# Execute the command to install Python dependencies listed in the requirements.txt file.

ENV ENV=prod
# Set the ENV environment variable to 'prod'. This value can be used in your application
# to define the working environment.

CMD python -m pytest -s --alluredir=test_results/ /tests_project/tests/
# Start the default command when the container starts. Here pytest is run to execute the tests,
# located in the /tests_project/tests/ directory. Test results are stored in the test_results/ directory inside the container.





