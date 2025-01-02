from django.contrib.auth import get_user_model


User = get_user_model()


class BaseOverrideRequestData:
    def override_request_data(self, request):
        if hasattr(request.data, "_mutable") and request.data._mutable is False:
            request.data._mutable = True
        request.data.update(self.get_overriding_data())
        return request

    def get_overriding_data(self):
        raise NotImplementedError()


class OverrideCreateRequestData(BaseOverrideRequestData):
    def create(self, request, *args, **kwargs):
        request = self.override_request_data(request)
        response = super().create(request, *args, **kwargs)
        return response


class OverrideUpdateRequestData(BaseOverrideRequestData):
    def update(self, request, *args, **kwargs):
        request = self.override_request_data(request)
        response = super().update(request, *args, **kwargs)
        return response


class OverrideRequestData(
    OverrideCreateRequestData,
    OverrideUpdateRequestData,
):
    pass
