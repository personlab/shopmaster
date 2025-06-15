from django.db import models

from django.utils.safestring import mark_safe

class Game(models.Model):
		rank = models.PositiveIntegerField(
				verbose_name='Позиция в рейтинге', unique=True, help_text='Номер позиции в топе (1, 2, 3...)'
		)
		title = models.CharField(verbose_name='Название игры', max_length=100)
		description = models.CharField(verbose_name='Описание', max_length=200)
		image = models.ImageField(verbose_name='Изображение игры', upload_to='image/', help_text='Рекомендуемый размер: 300x300px')
		link = models.URLField(max_length=200, blank=True, null=True, verbose_name='Ссылка для картинки')
		is_active = models.BooleanField(verbose_name='Активно', default=True)
		created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

		class Meta:
				verbose_name = 'Игра'
				verbose_name_plural = 'Игры'
				ordering = ['rank']

		def __str__(self):
				return f"{self.rank}. {self.title}"

		def image_tag(self):
				if self.image:
						return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
				return "Нет изображения"
		image_tag.short_description = 'Превью'
