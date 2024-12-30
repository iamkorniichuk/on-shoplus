from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from environs import Env
from playwright.sync_api import sync_playwright

from commons.shoplus import Shoplus


@api_view(["GET"])
def search_shop(request):
    query = request.query_params.get("query")
    country = request.query_params.get("country").upper()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()

        shoplus = Shoplus(context)

        username, password = load_credentials("credentials.env")
        shoplus.login(username, password)

        data = shoplus.search_shop(
            query,
            country=country,
        )
    return Response(data, status=status.HTTP_200_OK)


def load_credentials(env_file):
    env = Env()
    env.read_env(env_file)

    username = env.str("SHOPLUS_USERNAME")
    password = env.str("SHOPLUS_PASSWORD")

    return username, password
