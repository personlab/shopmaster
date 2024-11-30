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
	


class Featured(models.Model):
	title = models.CharField(max_length=200, verbose_name='Заголовок')
	image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Картинка')
	link = models.URLField(max_length=200, blank=True, null=True, verbose_name='Ссылка')
	reading_time = models.CharField(max_length=20, default='3 mins read', verbose_name='Время чтения')
	author_name = models.CharField(max_length=100, verbose_name='Имя автора')
	author_image = models.ImageField(upload_to='author_images/', blank=True, null=True, verbose_name='Изображение автора')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
			db_table = 'featured'
			verbose_name = 'в избранные'
			verbose_name_plural = 'Избранные'

	def __str__(self):
			return self.title