from django.contrib import admin
from buddy_groups.models import *

class buddy_members_inline(admin.TabularInline):
    model = GroupMembers
    extra = 1

class group_admins_inline(admin.TabularInline):
    model = GroupAdmins
    extra = 1
@admin.register(BuddyGroup)
class BuddyGroupAdmin(admin.ModelAdmin):
    # filter_horizontal = ("group_members",)
    inlines = (buddy_members_inline, group_admins_inline,)

admin.site.register(GroupMembers)
admin.site.register(GroupAdmins)
