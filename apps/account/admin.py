from django.contrib import admin
from apps.account.models import AccountModel, FollowerModel
# Register your models here.

admin.site.register(AccountModel)

class FollowerModelAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('user', 'follower')
        }),
    )
    list_display = ('user', 'follower')
    list_filter = ('user', 'follower')
    ordering = ('user', 'follower')


admin.site.register(FollowerModel, FollowerModelAdmin)
