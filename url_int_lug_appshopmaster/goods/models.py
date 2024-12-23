from itertools import product
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
		name = models.CharField(max_length=150, unique=True, verbose_name='Название')  # Название продукта
		slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')  # название в ссылке
		description = models.TextField(blank=True, null=True, verbose_name='Описание')  # Описание товара
		image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение') # Изображение товара
		price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена') # Цена товара
		discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %') # Скидка
		quantity = models.PositiveIntegerField(default=0, verbose_name='Количество') # Количество
		category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория') # Категория

		# class Meta, вложенный класс меняет название на синих полях и параметрах в них
		class Meta:
				db_table = 'product'
				verbose_name = 'Продукт'							# перевод на русский язык в единственном числе это отображается в title страницы.
				verbose_name_plural = 'Продукты'			# перевод на русский язык во множественном числе, отображается в меню админки.
				ordering = ("id",)	# Указываем пагинации как сортировать

		def __str__(self):
				return f"{self.name} - Количество: {self.quantity}"
		
		# Отображение ID товара
		def display_id(self):
			return f"{self.id:05}"
		
		"""
		Расчет стоимости с учетом скидки: Если self.discount действительно существует (например, не равно нулю и не является ложным значением), функция возвращает расчетную цену. Этот расчет выполняется следующим образом:
    - self.price — это исходная цена товара.
    - self.price * self.discount / 100 — рассчитывается величина скидки, исходя из процента self.discount.
    - self.price - (self.price * self.discount / 100) — из исходной цены вычитается сумма скидки.
    - round(..., 2) округляет полученную цену до двух знаков после запятой.
		
		"""
		def sell_price(self):
			if self.discount:
				return round(self.price - self.price*self.discount/100, 2)
			
			return self.price
		

		def get_main_image(self):
			main_image = self.images.filter(is_main=True).first()
			if not main_image:
				main_image = self.images.first()
			return main_image
		

		def __str__(self):
			return self.name
		
	

class ProductsImage(models.Model):
		product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images', verbose_name='Продукт')
		image = models.ImageField(upload_to='goods_images', verbose_name='Изображение')
		is_main = models.BooleanField(default=False, verbose_name='Главное изображение')


		def save(self, *args, **kwargs):
				if self.is_main: # Обновляем другие изображения, чтобы они небыли главными 
						ProductsImage.objects.filter(product=self.product, is_main=True).exclude(pk=self.pk).update(is_main=True)
				super().save(*args, **kwargs)


		def __str__(self):
			return f"{self.product.name} Image"
		
		"""
		class Meta, вложенный класс меняет название на синих полях и парвметрах в них 
		"""
		class Meta:
			verbose_name = "Изображение товара"
			verbose_name_plural = "Изображение"