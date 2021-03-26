from django.contrib import admin
from django.contrib.auth.models import User
from . import models


@admin.register(models.TypeUser)
class UserAdmin(admin.ModelAdmin):
    """
    Надстройка админ панели для модели пользователя
    """
    list_display = ('user', 'confirmation_email', 'api_key')

    list_filter = ('confirmation_email',)

    fieldsets = (
        ('Инфорамция о пользователе', {
            'fields': ('user', 'confirmation_email', )
        }),

    )
    search_fields = ('user', 'api_key',)
    ordering = ('confirmation_email', 'user',)


@admin.register(models.ApiRequestsHistory)
class HistoryAdmin(admin.ModelAdmin):
    """
    Надстройка админ панели для модели истории обращений к API
    """

    list_display = ('addr', 'api_key', 'date_request', 'status')

    list_filter = ('status', 'addr', 'owner_api_key_id', 'date_request')

    search_fields = ('addr', 'api_key',)

    ordering = ('date_request',)