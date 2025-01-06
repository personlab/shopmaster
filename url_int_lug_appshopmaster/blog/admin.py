from django.contrib import admin

from django.contrib import admin
from .models import Post, Hero, Featured, Tag, RecentPost


class PostAdmin(admin.ModelAdmin):
		list_display = ('title', 'created_at')
		search_fields = ('title',)
		prepopulated_fields = {'slug': ('title',)}
		list_filter = ('created_at',)

admin.site.register(Post, PostAdmin)


class RecentPostAdmin(admin.ModelAdmin):
		list_display = ('title', 'created_at')
		search_fields = ('title',)
		prepopulated_fields = {'slug': ('title',)}
		list_filter = ('created_at',)

admin.site.register(RecentPost, RecentPostAdmin)



class HeroAdmin(admin.ModelAdmin):
	list_display = ('id', 'image')


admin.site.register(Hero, HeroAdmin)


class FeaturedAdmin(admin.ModelAdmin):
	list_display = ('title', 'author_name', 'created_at')
	search_fields = ('title', 'author_name')
	list_filter = ('created_at',)

admin.site.register(Featured, FeaturedAdmin)



class TagAdmin(admin.ModelAdmin):
	list_display = ('name', 'popularity_count', 'image')
	list_filter = ('name',)
	search_fields = ('name',)

admin.site.register(Tag)