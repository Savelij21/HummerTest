from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# admin.site.register(User, UserAdmin)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('phone', 'invite_code', 'foreign_invite_code')
    list_display = ('id', 'phone', 'invite_code', 'foreign_invite_code')
    list_display_links = ('id', 'phone', 'invite_code', 'foreign_invite_code')
