import configuration
import requests
import data
def get_docs():
    return requests.get(configuration.URL_SERVICE + configuration.DOC_PATH)
def get_logs():
    return requests.get(configuration.URL_SERVICE + configuration.LOG_MAIN_PATH, params={"count": 20})
def get_users_table():
    return requests.get(configuration.URL_SERVICE + configuration.USERS_TABLE_PATH)
def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,  # подставляем полный url
                         json=body,  # тут тело
                         headers=data.headers)  # а здесь заголовки
def post_products_kits(products):
    return requests.post(configuration.URL_SERVICE + configuration.PRODUCTS_KITS_PATH,
                         json=products,
                         headers=data.headers)

# response = post_products_kits(data.product_ids);
# print(response.status_code)
# print(response.json())
# response = post_new_user(data.user_body);
# print(response.status_code)
# print(response.json())
# response = get_users_table()
# response = get_docs()
# print(response.status_code)
# print(response.headers)
