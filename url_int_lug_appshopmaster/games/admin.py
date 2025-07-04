from django.contrib import admin
from .models import Game


class GameAdmin(admin.ModelAdmin):
		list_display = ('rank', 'title', 'description', 'link', 'is_verified', 'image_tag', 'is_active')
		list_editable = ('is_active', 'link', 'is_verified')  # редактировать link прямо в списке
		list_filter = ('is_active', 'is_verified')
		search_fields = ('title', 'description')
		readonly_fields = ('image_tag',)
		fieldsets = (
				(None, {
						'fields': ('rank', 'title', 'description', 'link', 'is_active', 'is_verified')  # Добавлено is_verified
				}),
				('Изображение', {
						'fields': ('image', 'image_tag'),
						'classes': ('collapse',)
				}),
		)

admin.site.register(Game, GameAdmin)