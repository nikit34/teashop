from django.contrib import admin

from .models import Comment, ContactMessage


class CommentAdmin(admin.ModelAdmin):
    list_display = ('sender', 'msg', 'listing', 'send_time', 'active')
    list_filter = ('sender', 'send_time', 'active')
    search_fields = ('sender', 'msg')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Comment, CommentAdmin)


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'full_name', 'email', 'content')
    search_fields = ('full_name', 'email', 'content')
    readonly_fields = ('timestamp',)


admin.site.register(ContactMessage, ContactMessageAdmin)
