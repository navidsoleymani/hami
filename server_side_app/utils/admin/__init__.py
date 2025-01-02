from django.utils.translation import gettext_lazy as _
from django.contrib import admin


class BaseModelAdminClass(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.exclude_custom_updater()
        self.read_only_custom_updater()
        self.fieldsets_custom_updater()

    def exclude_custom_updater(self):
        exclude = self.exclude
        d_fields = [
            'is_deleted',
            'deleted_at',
            'deleted_by',
            'deleted_by_user_agent_info',
        ]

        if exclude is None:
            exclude = d_fields
        elif isinstance(exclude, tuple):
            exclude = list(exclude) + d_fields
        else:  # its list
            exclude = exclude + d_fields
        self.exclude = exclude

    def read_only_custom_updater(self):
        readonly_fields = self.readonly_fields
        d_fields = [
            'id',
            'created_at',
            'created_by',
            'created_by_user_agent_info',
            'updated_at',
            'last_updated_by',
            'last_updated_by_user_agent_info',
            'server_side_settings',
            'client_side_settings',
        ]
        if readonly_fields is None:
            readonly_fields = d_fields
        elif isinstance(readonly_fields, tuple):
            readonly_fields = list(readonly_fields) + d_fields
        else:  # its list
            readonly_fields = readonly_fields + d_fields
        self.readonly_fields = readonly_fields

    def fieldsets_custom_updater(self):
        fieldsets = self.fieldsets
        d_fields = [
            (_('Meta'), {'classes': ('collapse', 'close'), 'fields': [
                'id',
                ('created_by', 'created_at',),
                'created_by_user_agent_info',
                ('last_updated_by', 'updated_at',),
                'last_updated_by_user_agent_info',
            ]}),
            (_('Settings'), {'classes': ('collapse', 'close'), 'fields': [
                'server_side_settings',
                'client_side_settings',
            ]}),
        ]

        if fieldsets is None:
            pass
        elif isinstance(fieldsets, tuple):
            fieldsets = list(fieldsets) + d_fields
        else:  # its list
            fieldsets = fieldsets + d_fields
        self.fieldsets = fieldsets

    ordering = ('-created_at',)
