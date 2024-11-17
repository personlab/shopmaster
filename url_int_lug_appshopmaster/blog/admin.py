from django.contrib import admin

from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
		list_display = ('title', 'created_at')
		search_fields = ('title',)
		prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
