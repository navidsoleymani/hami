from django.contrib import admin

from .models import UserAgentDevice, UserAgentRequest

from django.utils.html import format_html


@admin.register(UserAgentDevice)
class UserAgentDeviceModelAdmin(admin.ModelAdmin):
    ordering = ('-created_dt',)
    permission_resource = "user_agent_device"
    list_display = (
        'ip',
        '_user_id',
        '_device_type',
        '_device',
        '_browser',
        '_os',
        '_t_rc',
        '_ltfh_rc',
        '_ph_rc',
        'created_dt',
    )
    list_display_links = (
        'ip',
        '_user_id',
        '_device_type',
        '_device',
        '_browser',
        '_os',
        '_t_rc',
        '_ltfh_rc',
        '_ph_rc',
        'created_dt',
    )
    search_fields = (
        'id',
        'user_id',
        'ip',
        'key',
    )
    list_filter = (
        'user_agent_is_mobile',
        'user_agent_is_tablet',
        'user_agent_is_touch_capable',
        'user_agent_is_pc',
        'user_agent_is_bot',
        'user_agent_browser_family',
        'user_agent_os_family',
        'user_agent_device_family',
    )
    readonly_fields = ('id', 'created_dt', 'key',)
    fieldsets = [
        ('Base Info', {'fields': [
            'user_id',
            'key',
            'ip',
        ]}),
        ('UserAgent', {'fields': [
            'user_agent_is_mobile',
            'user_agent_is_tablet',
            'user_agent_is_touch_capable',
            'user_agent_is_pc',
            'user_agent_is_bot',
            'user_agent_browser_family',
            'user_agent_browser_version',
            'user_agent_os_family',
            'user_agent_os_version',
            'user_agent_device_family',
            'user_agent_device_brand',
            'user_agent_device_model',
        ]}),
    ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def _user_id(self, obj):
        if obj.user_id:
            return obj.user_id
        return 'Anonymous'

    def _device_type(self, obj):
        pc = 'PC ' if obj.user_agent_is_pc else ''
        mobile = 'Mobile ' if obj.user_agent_is_mobile else ''
        tablet = 'Tablet ' if obj.user_agent_is_tablet else ''

        bot = 'Bot ' if obj.user_agent_is_bot else ''

        touch_capable = 'TouchCapable' if obj.user_agent_is_touch_capable else ''

        ret = pc + mobile + tablet + bot + touch_capable
        return ret if len(ret) else 'Unknown'

    def _browser(self, obj):
        return f'{obj.user_agent_browser_family} {obj.user_agent_browser_version}'

    def _os(self, obj):
        return f'{obj.user_agent_os_family} {obj.user_agent_os_version}'

    def _device(self, obj):
        return f'{obj.user_agent_device_family} {obj.user_agent_device_brand or ""} {obj.user_agent_device_model or ""}'

    def _t_rc(self, obj):
        return obj.requests.count()

    def _ltfh_rc(self, obj):
        from django.utils.timezone import now as dj_now, timedelta
        ltfh = dj_now() - timedelta(hours=24)

        return obj.requests.filter(created_dt__gte=ltfh).count()

    def _ph_rc(self, obj):
        from django.utils.timezone import now as dj_now, timedelta
        ph = dj_now() - timedelta(hours=1)

        return obj.requests.filter(created_dt__gte=ph).count()


@admin.register(UserAgentRequest)
class UserAgentRequestModelAdmin(admin.ModelAdmin):
    ordering = ('-created_dt',)
    permission_resource = "user_agent_request"
    list_display = (
        'uad',
        'created_dt',
        '_status',
        'endpoint',
        '_response_status_code',
        'rn',
        'rn_ph',
        'rn_24h',
    )

    search_fields = (
        'uad',
    )
    list_filter = (
        'status',
        'response_status_code',
    )
    fieldsets = [
        ('Base Info', {'fields': [
            'uad',
            ('method', 'endpoint', 'response_status_code',),

            'get',
            'headers',
            'cookies',

            ('rn', 'rn_ph', 'rn_24h',),
            ('status', 'status_color',),
            'created_dt',

        ]}),

    ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def _status(self, obj):
        return format_html(
            '<span style="background-color:{};">{}</span>',
            obj.status_color or 'withe',
            obj.status,
        )

    def _response_status_code(self, obj):
        response_status_code = obj.response_status_code
        response_status_code_color = 'withe'

        if 100 <= response_status_code < 200:
            response_status_code_color = '#8093f1'
        elif 200 <= response_status_code < 300:
            response_status_code_color = '#72ddf7'
        elif 300 <= response_status_code < 400:
            response_status_code_color = '#fdc5f5'
        elif 400 <= response_status_code < 500:
            response_status_code_color = '#f7aef8'
        elif 500 <= response_status_code < 600:
            response_status_code_color = '#b388eb'
        else:
            'withe'

        return format_html(
            '<span style="background-color:{};">{}</span>',
            response_status_code_color,
            response_status_code,
        )
