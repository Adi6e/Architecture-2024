import requests


def test_find_by_name(name: str, surname: str):
    url = f"http://localhost:5005/api/users/find_by_name?" \
        f"name={name}&" \
        f"surname={surname}"
    request = requests.get(url)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_find_by_login(login: str):
    url = f"http://localhost:5005/api/users/find_by_login?login={login}"
    request = requests.get(url)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_new_user(user_login: str, user_name: str, user_surname: str, user_password: str):
    data = {
        "user_login": user_login,
        "user_name": user_name,
        "user_surname": user_surname,
        "user_password": user_password
    }
    url = f"http://localhost:5005/api/users/new_user"
    request = requests.post(url=url, json=data)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_user_info(id: int):
    url = f"http://localhost:5005/api/users/info?id={id}"
    request = requests.get(url)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_delete_user(id: int):
    url = f"http://localhost:5005/api/users/delete?id={id}"
    request = requests.delete(url=url)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_update_user(user_id: int, user_login: str = None, user_name: str = None, user_surname: str = None, user_password: str = None):
    data = {
        "user_id": user_id,
        "user_login": user_login,
        "user_name": user_name,
        "user_surname": user_surname,
        "user_password": user_password
    }
    url = f"http://localhost:5005/api/users/update"
    request = requests.put(url=url, json=data)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_new_service(service_title: str, mongodb_id: str):
    data = {
        "service_title": service_title,
        "mongodb_id": mongodb_id,
    }
    url = f"http://localhost:5005/api/services/new_service"
    request = requests.post(url=url, json=data)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_get_all_services():
    url = f"http://localhost:5005/api/services/"
    request = requests.get(url=url)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_add_service_to_order(order_id: int, service_id: int):
    url = f"http://localhost:5005/api/services/add_service_to_order?"\
        f"order_id={order_id}&"\
        f"service_id={service_id}"
    request = requests.get(url=url)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


def test_get_services_by_order(order_id: int):
    url = f"http://localhost:5005/api/services/get_services_by_order?"\
        f"order_id={order_id}"
    request = requests.get(url=url)
    if request.status_code == 200:
        request_json = request.json()
        print(request_json)


test_user_info(id=1)
test_new_user(user_login="test", user_name="Test",
              user_surname="Testov", user_password="test123")
test_find_by_login(login="test")
test_find_by_name(name="Te", surname="Test")
test_delete_user(id=1)
test_update_user(user_id=11, user_login="test2")
test_new_service(service_title="New test service", mongodb_id="123asdsdaf31")
test_get_all_services()
test_add_service_to_order(order_id=1, service_id=1)
test_add_service_to_order(order_id=1, service_id=2)
test_add_service_to_order(order_id=1, service_id=3)
test_add_service_to_order(order_id=2, service_id=4)
test_add_service_to_order(order_id=2, service_id=5)
test_add_service_to_order(order_id=2, service_id=6)
test_add_service_to_order(order_id=3, service_id=7)
test_add_service_to_order(order_id=3, service_id=8)
test_add_service_to_order(order_id=3, service_id=9)
test_get_services_by_order(order_id=2)
