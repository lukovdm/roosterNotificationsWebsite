from django.contrib import admin
from register.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('number', 'email', 'updated')
    list_filter = ['updated']
    search_fields = ['number']

admin.site.register(User, UserAdmin)
