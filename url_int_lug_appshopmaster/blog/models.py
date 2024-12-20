from pyexpat import model
from tabnanny import verbose
from django.db import models
from django.utils.text import slugify


	# Модель для тегов

class Tag(models.Model):
		name= models.CharField(max_length=100, unique=True, verbose_name='Название тега')

		class Meta:
				db_table = 'tag'
				verbose_name = 'Тег'
				verbose_name_plural = 'Теги'

		def __str__(self):
				return self.name


	# Модель добавление постов

class Post(models.Model):
		title = models.CharField(max_length=200, verbose_name='Заголовок')
		slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
		content = models.TextField(verbose_name='Текст')
		image = models.ImageField(upload_to='image/', blank=True, null=True, verbose_name='Картинка')
		content_1 = models.TextField(verbose_name='Текст 1')
		image_1 = models.ImageField(upload_to='image/', blank=True, null=True, verbose_name='Изображение 1')
		content_2 = models.TextField(verbose_name='Текст 2')
		image_2 = models.ImageField(upload_to='image/', blank=True, null=True, verbose_name='Изображение 2')
		content_3 = models.TextField(verbose_name='Текст 3')
		image_3 = models.ImageField(upload_to='image/', blank=True, null=True, verbose_name='Изображение 3')
		tags = models.ManyToManyField(Tag, related_name='post', verbose_name='Теги')
		created_at = models.DateTimeField(auto_now_add=True)
		reading_time = models.IntegerField(default=0, verbose_name='Время чтения')
		author_name = models.CharField(max_length=100, verbose_name='Имя автора')

		class Meta:
				db_table = 'posts'
				verbose_name = 'пост'
				verbose_name_plural = 'Посты'

		def __str__(self):
				return self.title



	# Модель главного героя и приветствия на странице блог

class Hero(models.Model):
	subtitle = models.CharField(max_length=200, blank=True, null=True, verbose_name='Подзаголовок')
	title = models.CharField(max_length=200, verbose_name='Приветствие')
	content = models.TextField(verbose_name='Текст')
	image = models.ImageField(upload_to='image/', blank=True, null=True, verbose_name='Картинка героя')

	class Meta:
		db_table = 'hero'
		verbose_name = 'Картинку героя и приветствие'
		verbose_name_plural = 'Картинки героев и приветствие'

	def __str__(self):
		return self.image.url if self.image else 'Нет картинки'
	

	# Модель раздела избранный (featured)

class Featured(models.Model):
	title = models.CharField(max_length=200, verbose_name='Заголовок')
	image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Картинка')
	link = models.URLField(max_length=200, blank=True, null=True, verbose_name='Ссылка')
	reading_time = models.CharField(max_length=20, default='3 mins read', verbose_name='Время чтения')
	author_name = models.CharField(max_length=100, verbose_name='Имя автора')
	author_image = models.ImageField(upload_to='author_images/', blank=True, null=True, verbose_name='Изображение автора')
	created_at = models.DateTimeField(auto_now_add=True)
	# Добавляем связь с моделью Post
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='featured_items', null=True, blank=True)

	class Meta:
			db_table = 'featured'
			verbose_name = 'в избранные'
			verbose_name_plural = 'Избранные'

	def __str__(self):
			return self.title