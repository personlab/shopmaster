from tabnanny import verbose
from django.db import models
from django.utils.text import slugify

class Post(models.Model):
		title = models.CharField(max_length=200, verbose_name='Заголовок')
		slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
		content = models.TextField(verbose_name='Текст')
		image = models.ImageField(upload_to='image/', blank=True, null=True, verbose_name='Картинка')
		created_at = models.DateTimeField(auto_now_add=True)

		class Meta:
				db_table = 'posts'
				verbose_name = 'пост'
				verbose_name_plural = 'Посты'

		def save(self, *args, **kwargs):
				if not self.slug and self.title:
						original_slug = slugify(self.title)
						slug = original_slug
						number = 1
						while Post.objects.filter(slug=slug).exists():
								slug = f"{original_slug}-{number}"
								number += 1
						self.slug = slug
				super().save(*args, **kwargs)

		def __str__(self):
				return self.title
