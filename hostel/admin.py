
from __future__ import unicode_literals
from .models import Student, Room, Diff, Swap, Change
from django.contrib import admin
from django.contrib.auth.models import Group, User

admin.site.register(Student)
admin.site.register(Room)
admin.site.register(Diff)
admin.site.register(Swap)
admin.site.register(Change)
# customization of Django Admin
admin.site.unregister(Group)
admin.site.site_header='Hostel Management Dashboard'
