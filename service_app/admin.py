from django.contrib import admin
from django.contrib.auth.models import User
from . import models


@admin.register(models.TypeUser)
class UserAdmin(admin.ModelAdmin):
    # list_display = ('user', 'confirmation_email', 'api_key')

    # list_filter = ('confirmation_email',)
    fieldsets = (
        ('Инфорамция о пользователе', {
            'fields': ('confirmation_email', )
        }),

    )
    # list_filter = ('email', 'username', 'confirmation_email',)
    # fieldsets = (
    #     ('Инфорамция о пользователе',{
    #         'fields': (('email', 'username',), 'phone',  'confirmation_email')
    #     }),
    #
    # )
    # search_fields = ('email', 'username',)
    # ordering = ('username',)
