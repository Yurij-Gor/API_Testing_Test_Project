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

# Установка Java
RUN apt-get update && \
    apt-get install -y openjdk-21-jdk && \
    apt-get clean

# Установка Allure CLI
RUN wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.27.0/allure-commandline-2.27.0.tgz -O allure-commandline.tgz && \
    tar -zxvf allure-commandline.tgz -C /opt/ && \
    ln -s /opt/allure-2.27.0/bin/allure /usr/bin/allure && \
    rm -f allure-commandline.tgz

ENV ENV=prod
# Set the ENV environment variable to 'prod'. This value can be used in your application
# to define the working environment.

CMD python -m pytest -s --alluredir=test_results/ /tests_project/tests/
# Start the default command when the container starts. Here pytest is run to execute the tests,
# located in the /tests_project/tests/ directory. Test results are stored in the test_results/ directory inside the container.





