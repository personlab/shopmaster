from tabnanny import verbose
from unicodedata import category
from django.db import models

class Categories(models.Model):
		name = models.CharField(max_length=150, unique=True, verbose_name='Название')
		slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

		class Meta:
				db_table = 'category'
				verbose_name = 'Категорию'						# перевод на русский язык в единственном числе это отображается в title страницы.
				verbose_name_plural = 'Категории'		# перевод на русский язык во множественном числе, отображается в меню админки.

		def __str__(self):
				return self.name



class Products(models.Model):
		name = models.CharField(max_length=150, unique=True, verbose_name='Название')
		slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
		description = models.TextField(blank=True, null=True, verbose_name='Описание')
		image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')
		price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
		discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в процентах')
		quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
		category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')


		class Meta:
				db_table = 'product'
				verbose_name = 'Продукт'						# перевод на русский язык в единственном числе это отображается в title страницы.
				verbose_name_plural = 'Продукты'		# перевод на русский язык во множественном числе, отображается в меню админки.

		def __str__(self):
				return self.name