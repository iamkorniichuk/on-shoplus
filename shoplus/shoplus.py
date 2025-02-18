import requests

from .errors import *
from .rsa import Rsa
from .proxy import get_proxies


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


class Shoplus:
    def __init__(self, public_key):
        self.rsa = Rsa(public_key)

        self.proxies = get_proxies()
        self.token = None

    def login(self, username, password):
        url = "https://newapi.shoplus.net/api/v1/user/ocean/phone/password/login-auth"
        encrypted_password = self.rsa.encrypt(password)
        data = {
            "from_system": 14,
            "login_id": username,
            "login_type": 2,
            "password": encrypted_password,
            "req_type": "登录",
        }

        response = requests.post(
            url,
            json=data,
            proxies=self.proxies,
        ).json()
        if response["success"]:
            self.token = response["data"]["token"]

        error = response.get("errorCode") or response.get("error_code")

        if error == "PASSWORD_ERROR":
            raise AuthorizationError("Credentials are invalid")

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

        response = requests.get(
            url,
            params=params,
            headers=headers,
            proxies=self.proxies,
        ).json()
        if response["success"]:
            return self._parse_shops(response)

        error = response.get("errorCode") or response.get("error_code")

        if error == "TOKEN_INVALID":
            raise AuthorizationError("Token is expired")
        if error == "SUBSCRIBE_NOT_ALLOWED":
            raise SubscriptionError("Subscription is expired")
        if error == "SUBSCRIBE_TIMES_LIMITATIONS" or error == "REQUESTS_TOO_FREQUENT":
            raise QuotaError("Too many requests")

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
