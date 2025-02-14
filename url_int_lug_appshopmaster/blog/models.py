from pyexpat import model
from tabnanny import verbose
from django.db import models
from django.utils.text import slugify

from users.models import User
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



# Модель для тегов
class Tag(models.Model):
		name= models.CharField(max_length=100, unique=True, verbose_name='Название тега')
		image = models.ImageField(upload_to='tags/', null=True, blank=True, verbose_name='Изображение тега')
		popularity_count = models.PositiveIntegerField(default=0, verbose_name='Популярность тега')

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
		link = models.URLField(max_length=200, blank=True, null=True, verbose_name='Ссылка для кнопки')
		tags = models.ManyToManyField(Tag, related_name='post', verbose_name='Теги')
		created_at = models.DateTimeField(auto_now_add=True)
		reading_time = models.IntegerField(default=0, verbose_name='Время чтения')
		author_name = models.CharField(max_length=100, verbose_name='Имя автора')
		popularity_count = models.PositiveIntegerField(default=0, verbose_name='Популярность поста')
		is_archived = models.BooleanField(default=False, verbose_name='Архивировать')

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
	

		
# Модель для добавления Recent Post
class RecentPost(models.Model):
		subtitle = models.CharField(max_length=200, blank=True, null=True, verbose_name='Значок')
		title = models.CharField(max_length=200, verbose_name='Заголовок')
		slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
		content = models.TextField(verbose_name='Текст')
		image = models.ImageField(upload_to='image/', blank=True, null=True, verbose_name='Картинка')
		link = models.URLField(max_length=200, blank=True, null=True, verbose_name='Ссылка для кнопки')
		tags = models.ManyToManyField(Tag, related_name='recentpost', verbose_name='Теги')  # Добавлено это поле
		created_at = models.DateTimeField(auto_now_add=True)
		reading_time = models.IntegerField(default=0, verbose_name='Время чтения')
		author_name = models.CharField(max_length=100, verbose_name='Имя автора')
		popularity_count = models.PositiveIntegerField(default=0, verbose_name='Популярность поста')

		class Meta:
				db_table = 'posts Recent Post'
				verbose_name = 'в recent post'
				verbose_name_plural = 'Recent Post Game'

		def __str__(self):
				return self.title
		


# Модель раздела избранный (featured)
class Featured(models.Model):
	title = models.CharField(max_length=200, verbose_name='Заголовок')
	image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Картинка')
	link = models.URLField(max_length=200, blank=True, null=True, verbose_name='Ссылка')
	reading_time = models.CharField(max_length=20, default='3 mins read', verbose_name='Время чтения')
	author_name = models.CharField(max_length=100, default='admin', verbose_name='Имя автора')
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
	
	def save(self, *args, **kwargs):
		"""
		Переопределенный метод save. При обновлении записи в модели Featured
		подтягиваем время чтения из связанного поста (если пост выбран).
		"""
		if self.post:
				# Если пост выбран, обновляем reading_time и author_name
				self.reading_time = f"{self.post.reading_time} mins read"
				self.author_name = self.post.author_name
		elif not self.author_name:
				# Если имя автора не указано, используем "admin" по умолчанию
				self.author_name = "admin"
		super().save(*args, **kwargs)


class Comment(models.Model):
		post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)
		author = models.CharField(max_length=50, default='Anonymous')
		text = models.TextField(verbose_name='Текст комментария')
		created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
		author_image = models.CharField(max_length=255, blank=True, null=True)  # Поле для URL аватарки

		class Meta:
				db_table = 'comments'
				verbose_name = 'комментарий'
				verbose_name_plural = 'Комментарии'

		def __str__(self):
				if self.post:
						return f'Комментарий от {self.author} к посту {self.post.title}'
				return f'Комментарий от {self.author} (пост не указан)'
		
		def save(self, *args, **kwargs):
			# Убедимся, что created_at сохраняется в московском времени
			if not self.id:  # Если объект создается впервые
					self.created_at = timezone.localtime(timezone.now())
			super().save(*args, **kwargs)
		

# модель комментариев
class CommentRecentPost(models.Model):
		post = models.ForeignKey(RecentPost, on_delete=models.CASCADE, related_name='commentrecentpost_set', null=True)
		author = models.CharField(max_length=50, default='Anonymous')
		text = models.TextField(default='') 
		created_at = models.DateTimeField(auto_now_add=True)

		def __str__(self):
				return f'Comment by {self.author} on {self.post}'
				
