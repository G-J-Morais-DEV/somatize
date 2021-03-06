from django.contrib import admin

from .models import Thread, Reply


class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'modified']
    search_fields = ['title', 'author__email', 'body']
    prepopulated_fields = {'slug': ('title',)}


class ReplyAdmin(admin.ModelAdmin):
    list_display = ['thread', 'author', 'created_at', 'modified']
    search_fields = ['thread__title', 'author_email', 'reply']


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Reply, ReplyAdmin)
