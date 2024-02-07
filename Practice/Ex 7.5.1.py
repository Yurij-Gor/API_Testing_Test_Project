import requests
from json.decoder import JSONDecodeError

# List with different methods and values of method parametr
allowed_methods = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]
allowed_methods_final = ["GET", "POST", "PUT", "DELETE"]

for request_method in allowed_methods:
    for parameter_method in allowed_methods:
        if request_method == "GET":
            params = {"method": parameter_method}
            response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type",
                                    params=params)
        else:
            data = {"method": parameter_method}
            response = requests.request(request_method,
                                        "https://playground.learnqa.ru/ajax/api/compare_query_type",
                                        data=data)

        try:
            # Try to get success value from JSON
            success = response.json()["success"]
        except JSONDecodeError:
            # If an error occurs during decoding JSON, consider success = False
            success = False

        # Check the match of the query type and parameter value
        result = "OK" if  (request_method == parameter_method and success) or (
            request_method != parameter_method and not success) else "ОШИБКА"

        # Additional check when the server returns an error message "Wrong HTTP method"
        if request_method not in allowed_methods_final and response.status_code == 400 and "Wrong HTTP method" in response.text:
            result = "OK"

        # Additional check for cases when the method is not included in the list of acceptable returns status code 400
        if request_method not in allowed_methods_final and response.status_code == 400:
            result = "OK"

        print(f"Тип запроса: {request_method}, Значение параметра: {parameter_method} - {result}")
        print(response.text)
        print(response)
        print("\n")







