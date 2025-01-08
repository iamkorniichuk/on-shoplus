import time
import requests
import json
from urllib.parse import unquote
from playwright.sync_api import sync_playwright


COUNTRY_CODES = {
    "US": "United States",
    "GB": "United Kingdom",
    "ID": "Indonesia",
    "TH": "Thailand",
    "PH": "Philippines",
    "VN": "Viet Nam",
    "MY": "Malaysia",
    "SG": "Singapore",
}


class ShoplusError(Exception):
    pass


class AuthorizationError(ShoplusError):
    pass


class SubscriptionError(ShoplusError):
    pass


class QuotaError(ShoplusError):
    pass


class Shoplus:
    proxy = "91.196.7.209:3128"  # Free available proxy

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None

    def login(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(proxy={"server": f"http://{self.proxy}"})
            context = browser.new_context()

            timeout = 30_000
            context.set_default_timeout(timeout)

            page = context.new_page()
            page.goto("https://www.shoplus.net/login")

            username_input = page.locator('input[type="text"][autocomplete="on"]')
            username_input.fill(self.username)
            password_input = page.locator('input[type="password"]')
            password_input.fill(self.password)
            button = page.locator('button[type="button"]')
            button.click()

            page.wait_for_url("https://www.shoplus.net/home")

            for data in context.cookies():
                if data["name"] == "authorized-token":
                    value = unquote(data["value"])
                    self.token = json.loads(value)["accessToken"]

    def search_shop(self, query, country, size=20):
        assert country in COUNTRY_CODES.keys()

        params = {
            "keyword": query,
            "country_code": country,
            "sort": "43",
            "sort_type": "DESC",
            "size": size,
        }
        url = f"https://www.shoplus.net/api/v1/shop/search"
        headers = {"authorization": self.token}

        proxies = {
            "http": f"http://{self.proxy}",
            "https": f"http://{self.proxy}",
        }

        response = requests.get(url, params, headers=headers, proxies=proxies).json()
        if response["success"]:
            return self._parse_shops(response)

        error = response.get("errorCode") or response.get("error_code")

        if error == "TOKEN_INVALID":
            raise AuthorizationError()
        if error == "SUBSCRIBE_NOT_ALLOWED":
            raise SubscriptionError()
        if error == "SUBSCRIBE_TIMES_LIMITATIONS" or error == "REQUESTS_TOO_FREQUENT":
            raise QuotaError()

    def _parse_shops(self, data):
        results = []

        for shop in data:
            name = shop["shop_name"]
            categories = [c["category_name"] for c in shop["category_list"]]

            results.append(
                {
                    "name": name,
                    "categories": categories,
                }
            )

        return results
