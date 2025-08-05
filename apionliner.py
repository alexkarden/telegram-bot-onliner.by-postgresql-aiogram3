import logging
import os

import requests
from dotenv import (
    load_dotenv,
)

load_dotenv()


def make_request(url):
    access_token = get_token()
    if not access_token:
        logging.error("Failed to obtain access token.")
        return None

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json; charset=utf-8",
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        json_response = response.json()
        return json_response
    except requests.exceptions.HTTPError as http_err:
        logging.exception(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        logging.exception(f"Request error occurred: {req_err}")
        return None


def get_token():
    url = "https://b2bapi.onliner.by/oauth/token"

    headers = {
        "Accept": "application/json",
    }

    data = {
        "grant_type": "client_credentials",
    }

    # Чтение переменных окружения
    username = os.getenv("CLIENTID")
    password = os.getenv("CLIENSECRET")

    try:
        response = requests.post(
            url, headers=headers, data=data, auth=(username, password), timeout=5)

        if response.status_code == 200:
            result = response.json()
            access_token = result.get("access_token")
            if access_token:

                return access_token
            logging.error("Access token not found in the response.")
            return None
        logging.error(f"Failed to obtain token: {response.status_code} - "
                      f"{response.text}")
        return None

    except requests.exceptions.HTTPError as http_err:
        logging.exception(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        logging.exception(f"Request error occurred: {req_err}")
        return None


def get_order_list():
    url = "https://cart.api.onliner.by/orders"
    return make_request(url)


def get_order(orderKey):
    url = f"https://cart.api.onliner.by/orders/{orderKey}"
    return make_request(url)
