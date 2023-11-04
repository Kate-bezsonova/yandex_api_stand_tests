import configuration
import data
import requests


def get_new_user_header():
    user_for_kits_test = data.user_body.copy()  # копия тела для создания нового пользователя
    user_authToken = requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                                   json=user_for_kits_test,
                                   headers=data.headers)  # получили токен созданного пользователя
    kit_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + user_authToken.json()["authToken"]
    }
    return kit_headers


def post_new_user_kit(kit_body):  # создает набор у пользователя
    kit_request = requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_KIT,
                                json=kit_body,
                                headers=get_new_user_header())
    return kit_request


def get_kit_body(kit_name):  # меняет название набора в копии тела для запроса на создание набора
    current_body = data.kit_body.copy()
    current_body["name"] = kit_name
    return current_body


def positive_assert_test(kit_name):
    kit_body = get_kit_body(kit_name)
    kit_response = post_new_user_kit(kit_body)
    assert kit_response.status_code == 201
    assert kit_response.json()["name"] == kit_body["name"]


def negative_assert_test(kit_name):
    kit_body = get_kit_body(kit_name)
    kit_response = post_new_user_kit(kit_body)
    assert kit_response.status_code == 400


def test_create_kit_1_letter_in_name_get_success_response():
    positive_assert_test("a")


def test_create_kit_511_letter_in_name_get_success_response():
    kit_name = "Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab" \
               + "cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab" \
               + "cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab" \
               + "cdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab" \
               + "cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab" \
               + "cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC"
    positive_assert_test(kit_name)


def test_create_kit_no_name_get_error_response():
    kit_body = data.kit_body.copy()
    kit_body.pop("name")
    kit_response = post_new_user_kit(kit_body)
    assert kit_response.status_code == 400


def test_create_kit_512_letter_in_name_get_error_response():
    kit_name = "Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab" \
               + "cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab" \
               + "cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab" \
               + "cdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab" \
               + "cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab" \
               + "cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC"
    negative_assert_test(kit_name)


def test_create_kit_english_letter_in_name_get_success_response():
    positive_assert_test("QWErty")


def test_create_kit_russian_letter_in_name_get_success_response():
    positive_assert_test("Мария")


def test_create_kit_has_special_symbol_in_first_name_get_success_response():
    positive_assert_test("\"№%@\",")


def test_create_kit_has_space_in_name_get_success_response():
    positive_assert_test("Человек и КО")


def test_create_kit_has_number_in_name_get_success_response():
    positive_assert_test("123")


def test_create_kit_empty_name_get_error_response():
    negative_assert_test("")


def test_create_user_number_type_first_name_get_error_response():
    negative_assert_test(12)
