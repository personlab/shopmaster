from django.contrib import admin

from main.models import Slide


@admin.register(Slide)
class SlideAdmine(admin.ModelAdmin):
		list_display = ('animal_name',)
		search_fields = ('animal_name',)
