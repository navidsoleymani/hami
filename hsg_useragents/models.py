from django.utils.translation import gettext_lazy as _
from django.db import models


class UserAgentDevice(models.Model):
    key = models.CharField(
        verbose_name=_('Key'),
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
    )
    user_id = models.UUIDField(
        verbose_name=_('UserID'),
        blank=True,
        null=True,
    )
    user_agent_is_mobile = models.IntegerField(
        verbose_name=_('Mobile'),
        blank=True,
        null=True,
        choices=(
            (0, 'No'),
            (1, 'Yes'),
        ),
    )
    user_agent_is_tablet = models.IntegerField(
        verbose_name=_('Tablet'),
        blank=True,
        null=True,
        choices=(
            (0, 'No'),
            (1, 'Yes'),
        ),
    )
    user_agent_is_touch_capable = models.IntegerField(
        verbose_name=_('TouchCapable'),
        blank=True,
        null=True,
        choices=(
            (0, 'No'),
            (1, 'Yes'),
        ),
    )
    user_agent_is_pc = models.IntegerField(
        verbose_name=_('PC'),
        blank=True,
        null=True,
        choices=(
            (0, 'No'),
            (1, 'Yes'),
        ),
    )
    user_agent_is_bot = models.IntegerField(
        verbose_name=_('Bot'),
        blank=True,
        null=True,
        choices=(
            (0, 'No'),
            (1, 'Yes'),
        ),
    )
    user_agent_browser_family = models.CharField(
        verbose_name=_('BrowserFamily'),
        blank=True,
        null=True,
        max_length=255,
    )
    user_agent_browser_version = models.CharField(
        verbose_name=_('BrowserVersion'),
        blank=True,
        null=True,
        max_length=255,
    )
    user_agent_os_family = models.CharField(
        verbose_name=_('OSFamily'),
        blank=True,
        null=True,
        max_length=255,
    )
    user_agent_os_version = models.CharField(
        verbose_name=_('OSVersion'),
        blank=True,
        null=True,
        max_length=255,
    )
    user_agent_device_family = models.CharField(
        verbose_name=_('DeviceFamily'),
        blank=True,
        null=True,
        max_length=255,
    )
    user_agent_device_brand = models.CharField(
        verbose_name=_('DeviceBrand'),
        blank=True,
        null=True,
        max_length=255,
    )
    user_agent_device_model = models.CharField(
        verbose_name=_('DeviceModel'),
        blank=True,
        null=True,
        max_length=255,
    )
    ip = models.CharField(
        verbose_name=_('IP'),
        max_length=255,
        blank=True,
        null=True,
    )
    created_dt = models.DateTimeField(
        verbose_name=_('First Visit DateTime'),
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self):
        return f'{self.key}'

    class Meta:
        verbose_name = _('UserAgentDevice')
        verbose_name_plural = _('UserAgentDevices')


class UserAgentRequest(models.Model):
    uad = models.ForeignKey(
        verbose_name=_('UAD'),
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        to='UserAgentDevice',
        related_name='requests',
    )
    created_dt = models.DateTimeField(
        verbose_name=_('Created Datetime'),
        auto_now_add=True,
        db_index=True,
    )
    endpoint = models.TextField(
        verbose_name=_('Endpoint'),
        blank=False,
        null=False,
        default='',
    )
    response_status_code = models.IntegerField(
        verbose_name=_('Response Status code'),
        blank=False,
        null=False,
    )
    rn = models.IntegerField(
        verbose_name=_('RN'),
        blank=False,
        null=False,
        help_text=_('What is the request number?'),
        default=0,
    )
    rn_ph = models.IntegerField(
        verbose_name=_('RNPH'),
        blank=False,
        null=False,
        help_text=_('How many requests were made an hour ago?'),
        default=0,
    )
    rn_24h = models.IntegerField(
        verbose_name=_('RN24H'),
        blank=False,
        null=False,
        help_text=_('How many requests in the last 24 hours?'),
        default=0,
    )
    status_color = models.CharField(
        verbose_name=_('Status Color'),
        blank=False,
        null=False,
        default='#06d6a0',
        max_length=255,
    )
    status = models.CharField(
        verbose_name=_('Status'),
        blank=False,
        null=False,
        default='Normal',
        max_length=255,
    )
    method = models.CharField(
        verbose_name=_('Method'),
        blank=True,
        null=True,
        max_length=255,
    )
    get = models.JSONField(
        verbose_name=_('GET'),
        blank=True,
        null=True,
    )
    headers = models.JSONField(
        verbose_name=_('Headers'),
        blank=True,
        null=True,
    )
    cookies = models.JSONField(
        verbose_name=_('Cookies'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.endpoint}->{self.response_status_code}'

    class Meta:
        verbose_name = _('User Agent Request')
        verbose_name_plural = _('User Agent Requests')

    def save(self, **kwargs):
        from django.utils.timezone import now as dj_now, timedelta

        self.rn = self.uad.requests.count() + 1
        self.rn_ph = self.uad.requests.filter(created_dt__gte=dj_now() - timedelta(hours=1)).count() + 1
        self.rn_24h = self.uad.requests.filter(created_dt__gte=dj_now() - timedelta(hours=24)).count() + 1
        if 0 <= self.rn_ph < 50:
            self.status_color = '#06d6a0'
            self.status = 'Normal'
        elif 50 <= self.rn_ph < 100:
            self.status_color = '#ffba08'
            self.status = 'Busy'
        elif 100 <= self.rn_ph < 500:
            self.status_color = '#f48c06'
            self.status = 'Very Busy'
        else:
            self.status_color = '#d00000'
            self.status = 'Abnormal'
        super().save(**kwargs)
