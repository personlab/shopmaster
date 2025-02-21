from django.contrib import admin

from django.contrib import admin
from .models import Post, Hero, Featured, Tag, RecentPost, Comment
from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms

from django import forms
from .models import RecentPost


class PostAdminForm(forms.ModelForm):
		class Meta:
				model = Post
				fields = '__all__'
				widgets = {
						'content': CKEditor5Widget(config_name='default'),
				}

		def clean_content(self):
				content = self.cleaned_data.get('content')
				if not content or content.strip() == '':
						raise forms.ValidationError("Поле 'Текст' не может быть пустым.")
				return content


class PostAdmin(admin.ModelAdmin):
		list_display = ('title', 'created_at')
		search_fields = ('title', 'content')
		prepopulated_fields = {'slug': ('title',)}
		list_filter = ('created_at',)

admin.site.register(Post, PostAdmin)


class RecentPostAdminForm(forms.ModelForm):
		class Meta:
				model = RecentPost
				fields = '__all__'
				widgets = {
						'content': CKEditor5Widget(config_name='default'),
				}

		def clean_content(self):
				content = self.cleaned_data.get('content')
				if not content or content.strip() == '':
						raise forms.ValidationError("Поле 'Текст' не может быть пустым.")
				return content


class RecentPostAdmin(admin.ModelAdmin):
		list_display = ('title', 'created_at')
		search_fields = ('title', 'content')
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


class CommentAdmin(admin.ModelAdmin):
	list_display = ('author', 'get_post_title', 'created_at')  # Используем метод для отображения заголовка поста
	list_filter = ('author', 'created_at')
	search_fields = ('author', 'text')

	def get_post_title(self, obj):
			return obj.post.title if obj.post else 'Пост не указан'
	get_post_title.short_description = 'Заголовок поста'  # Название колонки в админке

admin.site.register(Comment, CommentAdmin)