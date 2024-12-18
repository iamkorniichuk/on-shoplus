from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from commons.shoplus import Shoplus


@api_view(["GET"])
def search_shop(request):
    query = request.query_params.get("query")
    country_code = request.query_params.get("country_code")
    size = request.query_params.get("size")

    shoplus = Shoplus()
    try:
        data = shoplus.search_shop(
            query,
            country_code=country_code,
            size=size,
        )
        return Response(data, status=status.HTTP_200_OK)
    except:
        error = None

    return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
