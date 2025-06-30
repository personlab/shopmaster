from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
		image = models.ImageField(
				upload_to='users_images', 
				blank=True, 
				null=True, 
				verbose_name='Аватар',
				default='users_images/baseavatar.jpg'
		)
		
		groups = models.ManyToManyField(
				'auth.Group',
				verbose_name='groups',
				blank=True,
				help_text='The groups this user belongs to.',
				related_name="custom_user_set",
				related_query_name="user",
				db_table='user_groups'
		)
		
		user_permissions = models.ManyToManyField(
				'auth.Permission',
				verbose_name='user permissions',
				blank=True,
				help_text='Specific permissions for this user.',
				related_name="custom_user_set",
				related_query_name="user",
				db_table='user_user_permissions'
		)
		
		class Meta:
				db_table = 'user'
				verbose_name = 'Пользователя'
				verbose_name_plural = 'Пользователи'

		def __str__(self):
				return f"{self.username} ({self.get_full_name()})"


class Wallet(models.Model):
		telegram_username = models.CharField(
				max_length=32,
				null=True,
				blank=True,
				verbose_name='Telegram логин'
		)
		address = models.CharField(
				max_length=128,
				db_index=True,
				unique=True,
				verbose_name='Адрес кошелька'
		)
		telegram_id = models.BigIntegerField(
				unique=True,
				null=True,
				blank=True,
				verbose_name='Telegram ID'
		)
		telegram_first_name = models.CharField(
				max_length=64,
				null=True,
				blank=True,
				verbose_name='Имя в Telegram'
		)
		telegram_last_name = models.CharField(
				max_length=64,
				null=True,
				blank=True,
				verbose_name='Фамилия в Telegram'
		)
		telegram_photo_url = models.URLField(
				max_length=512,
				null=True,
				blank=True,
				verbose_name='Аватар Telegram'
		)
		created_at = models.DateTimeField(
				auto_now_add=True,
				null=True,
				verbose_name='Дата создания'
		)
		last_login = models.DateTimeField(
				auto_now=True,
				verbose_name='Последний вход'
		)

		class Meta:
				verbose_name = 'Кошелек'
				verbose_name_plural = 'Кошельки'
				ordering = ['-created_at']

		def __str__(self):
				name = self.telegram_username or self.telegram_first_name or self.address[:10]
				return f"{name} ({self.address[:6]}...{self.address[-4:]})"