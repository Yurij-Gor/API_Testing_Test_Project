import requests  # Импортируем библиотеку requests для работы с HTTP-запросами
import time  # Импортируем библиотеку time для использования функции sleep()


# Функция для создания задачи и получения токена и времени ожидания
def create_task():
    url = "https://playground.learnqa.ru/ajax/api/longtime_job"
    response = requests.get(url)  # Отправляем GET-запрос на сервер для создания задачи
    result = response.json()  # Парсим ответ в формате JSON
    return result["token"], result["seconds"]  # Возвращаем токен и время ожидания


# Функция для проверки статуса задачи по токену
def check_task_status(task_token):
    url = f"https://playground.learnqa.ru/ajax/api/longtime_job"
    params = {"token": task_token}
    response = requests.get(url, params=params)  # Отправляем GET-запрос на сервер для проверки статуса задачи
    result = response.json()  # Парсим ответ в формате JSON

    # Проверка наличия поля "error"
    if "error" in result:
        error_message = result['error']
        print(f"Error: {error_message}")
        if error_message != "No job linked to this token":
            print("Unexpected error message")

        if error_message == "No job linked to this token":
            print("The error message is as expected")
        return error_message

    return result["status"]  # Возвращаем статус задачи


# Функция для ожидания выполнения задачи на указанное количество секунд
def wait_for_task_completion(seconds):
    print(f"Waiting for {seconds} seconds...")  # Выводим сообщение о времени ожидания
    time.sleep(seconds)  # Используем функцию sleep() для задержки выполнения программы


# Функция для получения результата задачи по токену
def get_task_result(task_token):
    url = f"https://playground.learnqa.ru/ajax/api/longtime_job"
    params = {"token": task_token}
    response = requests.get(url, params=params)  # Отправляем GET-запрос на сервер для получения результата задачи
    result = response.json()  # Парсим ответ в формате JSON

    # Проверка наличия поля "error"
    if "error" in result:
        error_message = result['error']
        print(f"Error: {error_message}")
        if error_message != "No job linked to this token":
            print("Unexpected error message")
        if error_message == "No job linked to this token":
            print("The error message is as expected")

        return error_message

    return result  # Возвращаем результат задачи


# Шаг 1: создаем задачу и получаем токен и время ожидания
token, wait_seconds = create_task()
print(f"Task created with token: {token}")

# Шаг 2: проверяем статус задачи до её завершения
status_before_waiting = check_task_status(token)
print(f"Status before waiting: {status_before_waiting}")

# Шаг 3: ждем нужное количество секунд
wait_for_task_completion(wait_seconds)

# Шаг 4: проверяем статус задачи после ожидания
status_after_waiting = check_task_status(token)
print(f"Status after waiting: {status_after_waiting}")

# Шаг 5: получаем результат задачи (если готова)
if status_after_waiting == "Job is ready":
    task_result = get_task_result(token)
    if "error" not in task_result:
        print(f"Task result: {task_result['result']}")
else:
    print("Job is NOT ready")

# Шаг 6: Проверяем запрос с неправильным токеном
print("\n")
print("Checking sending of invalid token in request:")
invalid_token = "QNyoDOQNzMQNiNQNiMQNyQNAQN"
invalid_token_result = check_task_status(invalid_token)
