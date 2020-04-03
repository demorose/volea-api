from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.models import User
from .models import List, Item, Profile

# Register your models here.

admin.site.register(List, SimpleHistoryAdmin)
admin.site.register(Item, SimpleHistoryAdmin)
admin.site.register(Profile, SimpleHistoryAdmin)
