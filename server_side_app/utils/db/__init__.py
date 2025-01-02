import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from config.utils.global_state import current_user_id, current_user_agent_info


class UUIDFieldContinuousCommunication(models.UUIDField):
    def __init__(
            self, auto_now=False, auto_now_add=False, ito=None, **kwargs
    ):
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add
        self.ito = ito
        super().__init__(**kwargs)

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = self.ito()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)


class JSONFieldContinuousCommunication(models.JSONField):
    def __init__(
            self, auto_now=False, auto_now_add=False, ito=None, **kwargs
    ):
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add
        self.ito = ito
        super().__init__(**kwargs)

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = self.ito()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)


class ForeignKeyContinuousCommunication(models.ForeignKey):
    def __init__(
            self, auto_now=False, auto_now_add=False, ito=None, **kwargs
    ):
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add
        self.ito = ito
        super().__init__(**kwargs)

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = self.ito()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)


class BaseSoftDeleteManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        # return all objects that their is_deleted are null
        return super().get_queryset().filter(is_deleted=False)

    def delete(self):
        from django.utils.timezone import now as dj_now

        return self.update(
            is_deleted=True,
            deleted_at=dj_now(),
            deleted_by=current_user_id(),
            deleted_by_user_agent_info=current_user_agent_info(),
        )


class SoftDeleteManager(BaseSoftDeleteManager.from_queryset(models.QuerySet)):
    pass


class SoftDeleteBaseModelClass(models.Model):
    is_deleted = models.BooleanField(
        verbose_name=_('Deleted'),
        blank=False,
        null=False,
        default=False,
        db_index=True,
        help_text=_('This field indicates whether this record has been deleted(soft delete) or not.'),
    )
    deleted_at = models.DateTimeField(
        verbose_name=_('Deleted Datetime'),
        blank=True,
        null=True,
        help_text=_('This field displays the date and time when this record was deleted(soft delete).'),
    )
    deleted_by = models.UUIDField(
        verbose_name=_('Deleted By...(ID)'),
        blank=True,
        null=True,
        help_text=_('This field displays who deleted(soft delete) the record.'),
    )
    deleted_by_user_agent_info = models.JSONField(
        verbose_name=_('Deleted By...(User Agent Info)'),
        blank=True,
        null=True,
        help_text=_('This field displays information about the user(user agent) who deleted(soft delete) this record.')
    )

    # enforce manager
    objects = SoftDeleteManager()

    def delete(self, **kwargs):
        from django.utils.timezone import now as dj_now

        self.is_deleted = True
        self.deleted_at = dj_now()
        self.deleted_by = current_user_id()
        self.deleted_by_user_agent_info = current_user_agent_info()
        self.save()

    def force_delete(self):
        super().delete()

    class Meta:
        abstract = True


class BaseModelClass(models.Model):
    id = models.UUIDField(
        verbose_name=_('ID'),
        primary_key=True,
        default=uuid.uuid4,
        blank=False,
        null=False,
        unique=True,
        editable=False,
        db_index=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created Datetime'),
        auto_now_add=True,
        help_text=_('This field indicates when and on what date this record was created.')
    )
    created_by = UUIDFieldContinuousCommunication(
        verbose_name=_('Created By...(ID)'),
        blank=True,
        null=True,
        auto_now_add=True,
        ito=current_user_id,
        help_text=_('This field indicates who created this record.'),
    )
    created_by_user_agent_info = JSONFieldContinuousCommunication(
        verbose_name=_('Created By...(User Agent Info)'),
        blank=True,
        null=True,
        auto_now_add=True,
        ito=current_user_agent_info,
        help_text=_('This field stores information about the user(user agent) who created this field.'),
    )

    updated_at = models.DateTimeField(
        verbose_name=_('Last Updated Datetime'),
        auto_now=True,
        help_text=_('This field displays the time and date this record was last updated.'),
    )
    last_updated_by = UUIDFieldContinuousCommunication(
        verbose_name=_('Last Updated By...(ID)'),
        blank=True,
        null=True,
        auto_now=True,
        ito=current_user_id,
        help_text=_('This field displays who last updated this record.'),
    )
    last_updated_by_user_agent_info = JSONFieldContinuousCommunication(
        verbose_name=_('Last Updated By...(User Agent Info)'),
        blank=True,
        null=True,
        auto_now=True,
        ito=current_user_agent_info,
        help_text=_('This field displays the information of the user(user agent) who last updated this record.')
    )

    server_side_settings = models.JSONField(
        verbose_name=_('Server-Side Settings'),
        blank=True,
        null=True,
        help_text=_(
            'If you need to have specific settings for each record in '
            'this table on the server side, '
            'you can save these settings in this section.'),
    )
    client_side_settings = models.JSONField(
        verbose_name=_('Client-Side Settings'),
        blank=True,
        null=True,
        help_text=_(
            'If you need to have specific settings for each record in '
            'this table on the client side, '
            'you can save these settings in this section.'),
    )

    class Meta:
        abstract = True

    history = HistoricalRecords(inherit=True)

    def __str__(self):
        return str(self.id)


class BaseDBModel(SoftDeleteBaseModelClass, BaseModelClass):
    class Meta:
        abstract = True

