class Shoplus:
    COUNTRIES_MAP = {
        "US": "United States",
        "GB": "United Kingdom",
        "ID": "Indonesia",
        "TH": "Thailand",
        "PH": "Philippines",
        "VN": "Viet Nam",
        "MY": "Malaysia",
        "SG": "Singapore",
    }
    _shops = None

    def __init__(self, context):
        self.context = context

    def login(self, username, password):
        self.context.clear_cookies()

        page = self.context.new_page()
        page.goto("https://www.shoplus.net/login")

        username_input = page.locator('input[type="text"][autocomplete="on"]')
        username_input.fill(username)
        password_input = page.locator('input[type="password"]')
        password_input.fill(password)
        button = page.locator('button[type="button"]')
        button.click()

        page.wait_for_url("https://www.shoplus.net/home")

    def search_shop(self, query, country):
        assert country in self.COUNTRIES_MAP.keys()

        def handle_api_request(route):
            route.continue_()

            response = route.request.response().json()

            if response["success"]:
                self._shops = self._parse_shops(response["data"])

            error_code = response.get("errorCode") or response.get("error_code")

            if error_code == "SUBSCRIBE_NOT_ALLOWED":
                raise Exception(
                    "SUBSCRIBE_NOT_ALLOWED` is returned. Try to call `.login()` first."
                )

        page = self.context.new_page()
        page.goto(f"https://www.shoplus.net/discovery/shop?keyword={query}")
        page.wait_for_load_state()

        page.route("https://www.shoplus.net/api/v1/shop/search?*", handle_api_request)

        country_name = self.COUNTRIES_MAP[country]
        country_divs = page.locator('div[title="Country"]').locator("div")
        country_button = country_divs.get_by_text(country_name, exact=True)

        country_button.wait_for()
        country_button.dispatch_event("click")

        return self._shops

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
