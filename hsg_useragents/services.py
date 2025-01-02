from django.utils.deprecation import MiddlewareMixin

from .models import UserAgentDevice, UserAgentRequest


class UserAgentDeviceMiddleware(MiddlewareMixin):

    def process_request(self, request):
        self.user_agent_device(request)
        setattr(request, 'uad', self.uad_schema)
        setattr(request, 'uad_obj', self.uad_obj)

    def process_response(self, request, response):
        self.process_request(request)

        response.set_cookie(
            key='UAD',
            value=request.uad.key,
            max_age=60 * 60 * 24 * 365,
            httponly=False,
            secure=False
        )
        self._create_user_agent_request_obj(request, response)
        return response

    def _get_user_agent_device_obj(self, adk, user_id):
        try:
            obj = UserAgentDevice.objects.get(key=adk)
            if obj.user_id is None and user_id is not None:
                obj = None
        except UserAgentDevice.DoesNotExist:
            obj = None
        return obj

    def _get_or_create_user_agent_device_obj(self, request):
        self.uad_schema = request
        try:
            obj = UserAgentDevice.objects.get(key=self.uad_schema.key)
        except UserAgentDevice.DoesNotExist:
            obj = UserAgentDevice.objects.create(**self.uad_schema.model_dump())
        except Exception as exc:
            raise exc.args[0]

        return obj

    def user_agent_device(self, request):

        cookie_name = 'UAD'
        if not hasattr(request, 'COOKIES'):
            return None

        user_id = request.user.id if (request.user and request.user.is_authenticated) else None

        adk = request.COOKIES.get(cookie_name)

        obj = (
                self._get_user_agent_device_obj(adk=adk, user_id=user_id) or
                self._get_or_create_user_agent_device_obj(request)
        )

        self.uad_schema = obj
        self.uad_obj = obj

    _uad_schema = None

    @property
    def uad_schema(self):
        return self._uad_schema

    @uad_schema.setter
    def uad_schema(self, inp):
        from .schemas import UADSchema

        self._uad_schema = UADSchema(inp)

    def _create_user_agent_request_obj(self, request, response):
        UserAgentRequest.objects.create(
            uad=request.uad_obj,
            endpoint=request.path,
            response_status_code=response.status_code,
            method=request.method if hasattr(request, 'method') else {},
            get=dict(request.GET) if hasattr(request, 'GET') else {},
            headers=dict(request.headers) if hasattr(request, 'headers') else {},
            cookies=dict(request.COOKIES) if hasattr(request, 'COOKIES') else {},
        )
