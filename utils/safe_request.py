import time

import requests

from exceptions import ApiConnectionError


def get_request_safe(url, headers, params=None, retry=5):
    """Делает несколько попыток выполнить get-запрос.
    Возбуждает исключение ApiConnectionError в случае неудачи.
    """

    try:
        response = requests.get(url=url, headers=headers, params=params)

    except Exception as ex:
        time.sleep(3)
        if retry:
            print(f"[INFO] ошибка запроса к api, retry={retry} = {url}")
            return get_request_safe(url, headers, params, retry=(retry - 1))
        else:
            raise ApiConnectionError
    else:
        return response
