from django.db import models

class Slide(models.Model):
		bg_image = models.ImageField(upload_to='slides/backgrounds/', verbose_name='Главная картинка backround')
		animal_name = models.CharField(max_length=200, verbose_name='Главные большые буквы')
		animal_image = models.ImageField(upload_to='slides/animals/', verbose_name='Маленькая картинка')
		caption = models.CharField(max_length=255, verbose_name='Текст над большими буквами')
		paragraph = models.TextField(verbose_name='Текст главной страницы параграф 1')
		paragraph_link = models.URLField(max_length=200, blank=True, null=True, verbose_name='Ссылка в параграфе')
		video = models.FileField(upload_to='slides/videos/')
		video_description = models.TextField(verbose_name='Текст модального окна видео')
		video_description_link = models.URLField(max_length=200, blank=True, null=True, verbose_name='Ссылка параграфа модального окна')

		class Meta:
				verbose_name = 'слайды и описание'
				verbose_name_plural = 'Слайды'

		def __str__(self):
				return self.animal_name
