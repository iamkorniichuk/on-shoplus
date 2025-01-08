from rest_framework.routers import SimpleRouter, Route


class SubscriptionRouter(SimpleRouter):
    routes = [
        Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={
                "get": "retrieve",
                "post": "create",
                "delete": "destroy",
            },
            name="{basename}",
            detail=True,
            initkwargs={"suffix": "Instance"},
        ),
    ]
