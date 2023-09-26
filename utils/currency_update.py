import json
import os.path
from datetime import date
from utils.safe_request import get_request_safe

PATH_TO_JSON = "data/exchange_rates.json"


def update_daily_rates():
    """Getting actual currency rates from api"""
    api_link: str = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = get_request_safe(
        api_link,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15"
        },
    )
    with open(PATH_TO_JSON, "w", encoding="utf-8") as json_out:
        result = {date.today().isoformat(): response.json()}
        json.dump(result, json_out, indent=4, ensure_ascii=False)
        return result


def get_current_rates() -> dict:
    """Returns actual currency rates for today"""
    today = date.today().isoformat()

    if not os.path.exists(PATH_TO_JSON):
        return update_daily_rates()[today]['Valute']

    with open(PATH_TO_JSON, "r", encoding="utf-8") as json_in:
        last_rates = json.load(json_in)

    if today not in last_rates.keys():
        last_rates = update_daily_rates()

    return last_rates[today]['Valute']
