FROM ubuntu:latest

# Installing Python, pip, wget, and python3-venv
RUN apt-get update && \
    apt-get install -y python3 python3-pip wget python3-venv locales && \
    apt-get clean

# Set up locale
RUN locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8

# Setting environment variables for locale
ENV LANG en_US.UTF-8

# Installing Java
RUN apt-get install -y openjdk-11-jdk && \
    apt-get clean;

# Setting environment variables for Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

WORKDIR /tests_project/

COPY requirements.txt .

# Creating a virtual environment and installing dependencies
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --upgrade pip
RUN /opt/venv/bin/pip install -r requirements.txt

# Installing Allure CLI
RUN wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.8/allure-commandline-2.13.8.tgz -O allure-commandline.tgz && \
    tar -zxvf allure-commandline.tgz -C /opt/ && \
    ln -s /opt/allure-2.13.8/bin/allure /usr/bin/allure && \
    rm -f allure-commandline.tgz

CMD ["/opt/venv/bin/python", "-m", "pytest", "-s", "--alluredir=test_results/", "/tests_project/tests/"]
