import json
import urllib.parse as url_parse

from environs import Env
from playwright.sync_api import sync_playwright


env = Env()
env.read_env("credentials.env")


def get_token(context):
    for cookie in context.cookies(["https://www.shoplus.net"]):
        if cookie["name"] == "authorized-token":
            value = url_parse.unquote(cookie["value"])
            data = json.loads(value)
            token = data["accessToken"]
            return token


class Shoplus:
    retries = 5

    username = None
    password = None
    token = None

    def authenticate(self):
        if not self.username or not self.password:
            self.load_credentials()
        if not self.token:
            self.update_token()

    def update_token(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()

            page = context.new_page()
            page.goto("https://www.shoplus.net/login")

            username_input = page.locator('input[type="text"][autocomplete="on"]')
            username_input.fill(self.username)
            password_input = page.locator('input[type="password"]')
            password_input.fill(self.password)
            button = page.locator('button[type="button"]')
            button.click()

            page.wait_for_url("https://www.shoplus.net/home")
            self.token = get_token(page.context)
            browser.close()

    def load_credentials(self):
        self.username = env.str("SHOPLUS_USERNAME")
        self.password = env.str("SHOPLUS_PASSWORD")
