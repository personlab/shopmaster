from pyexpat import model
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

		def __str__(self):
				return self.title



class Hero(models.Model):
	image = models.ImageField(upload_to='image/', blank=True, null=True, verbose_name='Картинка героя')

	class Meta:
		db_table = 'hero'
		verbose_name = 'Картинку героя'
		verbose_name_plural = 'Картинки героев'

	def __str__(self):
		return self.image.url if self.image else 'Нет картинки'