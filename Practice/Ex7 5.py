import requests
from json.decoder import JSONDecodeError

# Список с разными методами и значениями параметра method
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
                                        " ",
                                        data=data)

        try:
            # Попытка получить значение success из JSON
            success = response.json()["success"]
        except JSONDecodeError:
            # Если возникает ошибка при декодировании JSON, считаем, что success = False
            success = False

        # Проверка соответствия типа запроса и значения параметра
        result = "ОК" if (request_method == parameter_method and success) or (
                request_method != parameter_method and not success) else "ОШИБКА"

        # Дополнительная проверка для случаев, когда сервер возвращает сообщение об ошибке "Wrong HTTP method"
        if request_method not in allowed_methods_final and response.status_code == 400 and "Wrong HTTP method" in response.text:
            result = "ОК"

        # Дополнительная проверка для случаев, когда метод не входящий список допустимых возвращает статус код 400
        if request_method not in allowed_methods_final and response.status_code == 400:
            result = "ОК"

        print(f"Тип запроса: {request_method}, Значение параметра: {parameter_method} - {result}")
        print(response.text)
        print(response)
        print("\n")
