import json
import requests
from urllib.parse import unquote

from environs import Env
from random_user_agent.user_agent import UserAgent
from playwright.sync_api import sync_playwright


env = Env()
env.read_env("credentials.env")


class Shoplus:
    retries = 3

    username = None
    password = None

    token = None
    cookies = None
    session_id = None
    device_id = None
    user_id = None

    def search_shop(self, query, country_code=None, size=10):
        if (
            not self.token
            or not self.session_id
            or not self.device_id
            or not self.user_id
        ):
            self.authenticate()

        params = {
            "cursor": 0,
            "sort": 43,
            "sort_type": "DESC",
            "size": size,
            "keyword": query,
            "country_code": country_code,
        }
        headers = {
            "authorization": self.token,
            "user-id": self.user_id,
            "device-id": self.device_id,
            "session-id": self.session_id,
            "system-id": "14",
            "User-Agent": UserAgent().get_random_user_agent(),
            "Referer": f"https://www.shoplus.net/discovery/shop?keyword={query}",
        }

        for _ in range(self.retries):
            response = requests.get(
                "https://www.shoplus.net/api/v1/shop/search",
                params=params,
                headers=headers,
            ).json()
            print(response)

            if response["success"]:
                shops = self._parse_shops(response)
                return shops

            error_code = response.get("errorCode") or response.get("error_code")

            if error_code.isspace():
                pass
            elif error_code == "REQUESTS_TOO_FREQUENT":
                self.rotate_vpn()
            elif error_code == "SUBSCRIBE_NOT_ALLOWED":
                self.authenticate()

    def rotate_vpn(self):
        pass

    def _parse_shops(self, response_json):
        shops = []

        for data in response_json["data"]:
            name = data["shop_name"]
            categories = [c["category_name"] for c in data["category_list"]]

            shops.append(
                {
                    "name": name,
                    "categories": categories,
                }
            )

        return shops

    def authenticate(self):
        if not self.username or not self.password:
            self.load_credentials()
        self.update_auth_context()

    def update_auth_context(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()

            self.login(page)

            self.update_token(page)
            self.update_headers(page)

            browser.close()

    def login(self, page):
        page.goto("https://www.shoplus.net/login")

        username_input = page.locator('input[type="text"][autocomplete="on"]')
        username_input.fill(self.username)
        password_input = page.locator('input[type="password"]')
        password_input.fill(self.password)
        button = page.locator('button[type="button"]')
        button.click()

        page.wait_for_url("https://www.shoplus.net/home")

    def update_headers(self, page):
        def handle_route(route):
            request = route.request

            self.user_id = request.header_value("user-id")
            self.session_id = request.header_value("session-id")
            self.device_id = request.header_value("device-id")

            route.continue_()

        page.route("https://www.shoplus.net/api/v1/shop/search?*", handle_route)
        page.goto("https://www.shoplus.net/discovery/shop")
        page.wait_for_timeout(30_000)  # TODO: Change

    def update_token(self, page):
        for cookie in page.context.cookies(["https://www.shoplus.net"]):
            if cookie["name"] == "authorized-token":
                value = unquote(cookie["value"])
                data = json.loads(value)
                self.token = data["accessToken"]
                break

    def load_credentials(self):
        self.username = env.str("SHOPLUS_USERNAME")
        self.password = env.str("SHOPLUS_PASSWORD")
