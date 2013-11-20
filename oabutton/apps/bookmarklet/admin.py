from django.contrib import admin
from oabutton.apps.bookmarklet.models import OAUser, OAEvent


class OAUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'profession', 'mailinglist')

class OAEventAdmin(admin.ModelAdmin):
    list_display = ('doi', 'url', 'user_email', 'user_name')

admin.site.register(OAUser, OAUserAdmin)
admin.site.register(OAEvent, OAEventAdmin)
