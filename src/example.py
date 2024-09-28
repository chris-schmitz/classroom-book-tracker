import requests


def multiply_n_numbers(*numbers: int) -> int:
    product = 1
    for number in numbers:
        product *= number

    return product


def get_book_list():
    response = requests.get("http://www.somebooksearch.biz/search")
    data = response.json()
    return data["books"]


def update_book(payload):
    requests.post("http://www.somebooksearch.biz/search", json=payload)
