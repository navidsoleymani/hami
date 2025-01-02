from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from .utils.admin import BaseModelAdminClass as Parent

from .models import (
    Goal as GoalModel,
    FollowerCount as FollowerCountModel,
)


@admin.register(GoalModel)
class GoalModelAdmin(Parent):
    list_display = [
        'user_id',
        'follower_count',
        'telegram_user',
    ]
    list_display_links = [
        'user_id',
        'follower_count',
        'telegram_user',
    ]
    search_fields = [
        'user_id',
        'telegram_user',
    ]
    fieldsets = [
        (_('Info'), {
            'fields': [
                'user_id',
                'follower_count',
                'telegram_user',
            ]}),
    ]


@admin.register(FollowerCountModel)
class FollowerCountModelAdmin(Parent):
    list_display = [
        'goal',
        'followers',
    ]
    list_display_links = [
        'goal',
        'followers',
    ]
    fieldsets = [
        (_('Info'), {
            'fields': [
                'goal',
                'followers',
            ]}),
    ]
