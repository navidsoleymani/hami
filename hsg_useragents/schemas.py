from django.http.request import HttpRequest
from pydantic import BaseModel
from datetime import datetime
from hashlib import md5
from uuid import UUID

from .models import UserAgentDevice


def _user_agent_device_key_creator(**kwargs):
    str_ = (
        f"{kwargs.get('user_id')}-"
        f"{kwargs.get('user_agent_is_mobile')}-"
        f"{kwargs.get('user_agent_is_tablet')}-"
        f"{kwargs.get('user_agent_is_touch_capable')}-"
        f"{kwargs.get('user_agent_is_pc')}-"
        f"{kwargs.get('user_agent_is_bot')}-"
        f"{kwargs.get('user_agent_browser_family')}-"
        f"{kwargs.get('user_agent_browser_version')}-"
        f"{kwargs.get('user_agent_os_family')}-"
        f"{kwargs.get('user_agent_os_version')}-"
        f"{kwargs.get('user_agent_device_family')}-"
        f"{kwargs.get('user_agent_device_brand')}-"
        f"{kwargs.get('user_agent_device_model')}-"
        f"{kwargs.get('ip')}"
    )
    ret = str(md5(str_.encode('utf-8')).hexdigest())
    return ret


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class UADSchema(BaseModel):
    def __init__(self, value):
        kw = {}
        if isinstance(value, UserAgentDevice):
            kw = {
                'id': value.id,
                'user_id': value.user_id,
                'user_agent_is_mobile': value.user_agent_is_mobile,
                'user_agent_is_tablet': value.user_agent_is_tablet,
                'user_agent_is_touch_capable': value.user_agent_is_touch_capable,
                'user_agent_is_pc': value.user_agent_is_pc,
                'user_agent_is_bot': value.user_agent_is_bot,
                'user_agent_browser_family': value.user_agent_browser_family,
                'user_agent_browser_version': value.user_agent_browser_version,
                'user_agent_os_family': value.user_agent_os_family,
                'user_agent_os_version': value.user_agent_os_version,
                'user_agent_device_family': value.user_agent_device_family,
                'user_agent_device_brand': value.user_agent_device_brand,
                'user_agent_device_model': value.user_agent_device_model,
                'ip': value.ip,
                'key': value.key,
                'created_dt': value.created_dt,
            }
        if isinstance(value, HttpRequest):
            kw = {
                'user_id': value.user.id if value.user and value.user.is_authenticated else None,
                'ip': get_client_ip(value)
            }
            if hasattr(value, 'user_agent'):
                user_agent = value.user_agent

                kw['user_agent_is_mobile'] = user_agent.is_mobile
                kw['user_agent_is_tablet'] = user_agent.is_tablet
                kw['user_agent_is_touch_capable'] = user_agent.is_touch_capable
                kw['user_agent_is_pc'] = user_agent.is_pc
                kw['user_agent_is_bot'] = user_agent.is_bot
                kw['user_agent_browser_family'] = user_agent.browser.family
                kw['user_agent_browser_version'] = user_agent.browser.version_string
                kw['user_agent_os_family'] = user_agent.os.family
                kw['user_agent_os_version'] = user_agent.os.version_string
                kw['user_agent_device_family'] = user_agent.device.family
                kw['user_agent_device_brand'] = user_agent.device.brand
                kw['user_agent_device_model'] = user_agent.device.model

            kw['key'] = _user_agent_device_key_creator(**kw)
        super().__init__(**kw)

    id: int | None = None
    user_id: int | UUID | None = None
    user_agent_is_mobile: bool | None = None
    user_agent_is_tablet: bool | None = None
    user_agent_is_touch_capable: bool | None = None
    user_agent_is_pc: bool | None = None
    user_agent_is_bot: bool | None = None
    user_agent_browser_family: str | None = None
    user_agent_browser_version: str | None = None
    user_agent_os_family: str | None = None
    user_agent_os_version: str | None = None
    user_agent_device_family: str | None = None
    user_agent_device_brand: str | None = None
    user_agent_device_model: str | None = None
    ip: str | None = None

    key: str | None = None

    created_dt: datetime | None = None

    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'is_mobile': self.user_agent_is_mobile,
            'is_tablet': self.user_agent_is_tablet,
            'is_touch_capable': self.user_agent_is_touch_capable,
            'is_pc': self.user_agent_is_pc,
            'is_bot': self.user_agent_is_bot,
            'browser_family': self.user_agent_browser_family,
            'browser_version': self.user_agent_browser_version,
            'os_family': self.user_agent_os_family,
            'os_version': self.user_agent_os_version,
            'device_family': self.user_agent_device_family,
            'device_brand': self.user_agent_device_brand,
            'device_model': self.user_agent_device_model,
            'ip': self.ip,
            'key': self.key,
            'created_dt': str(self.created_dt),
        }
