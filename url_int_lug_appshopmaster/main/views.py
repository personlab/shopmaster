from turtle import title
from django.http import HttpResponse
from django.shortcuts import render
from django.template import context

from goods import views
from goods.models import Categories
from main.models import Slide

#  С применением классов
from django.views import View


class IndexView(View):
		def get(self, request):
			slides = Slide.objects.all() # извлекаем все слайды из базы данных
			context = {
				'title': 'TonGameApp - Главная',
				'slides': slides
			}
			return render(request, 'main/index.html', context=context)
		

# class IndexView(View):

# 	def get(self, request):
# 		context = {
# 			'title': 'Home - Главная',
# 			'slides': [
# 					{
# 							'bg_image': 'deps/images/bg-1-1.png',
# 							'animal_name': 'Goblin Mine',
# 							'animal_image': 'deps/images/animal-1-1.png',
# 							'caption': 'Собирай целые горы золота',
# 							'paragraph': 'Goblin Mine Game – это захватывающая экономическая игра, в которой вы можете стать настоящим магнатом в мире гоблинов! Погрузитесь в уникальную атмосферу фантастической шахты, добывайте редкие ресурсы, управляйте гоблинскими рабочими и развивайте свои активы.',
# 							'video': 'deps/videos/animal-video-1.mp4',
# 							'video_description': 'Игра предлагает увлекательный симбиоз стратегии и экономики: выбирайте оптимальные стратегии для достижения успеха, улучшайте технологии и расширяйте свои владения.'
# 					},
# 					{
# 							'bg_image': 'deps/images/bg-2-2.jpg',
# 							'animal_name': 'CITY HOLDER',
# 							'animal_image': 'deps/images/animal-2-2.png',
# 							'caption': 'Выбери свой стиль игры: стелс или штурм',
# 							'paragraph': 'В мире, охваченном кризисами и катастрофами, City Holder предлагает вам шанс построить свое собственное будущее. Создавайте и управляйте своим городом, зарабатывайте токены за внутриигровую активность и просто наслаждайтесь опытом!',
# 							'video': 'deps/videos/animal-video-2.mp4',
# 							'video_description': 'Наш токен $CITY скоро будет доступен на основных криптовалютных биржах, что предоставит еще больше возможностей.'
# 					},
# 					{
# 							'bg_image': 'deps/images/bg-3.jpg',
# 							'animal_name': 'Red FOX',
# 							'animal_image': 'deps/images/animal-3.png',
# 							'caption': 'Wildlife Nature',
# 							'paragraph': 'Давно выяснено, что при оценке дизайна и композиции читаемый текст мешает',
# 							'video': 'deps/videos/animal-video-3.mp4',
# 							'video_description': 'Давно выяснено, что при оценке дизайна'
# 					},
# 					{
# 							'bg_image': 'deps/images/bg-4.jpg',
# 							'animal_name': 'Parrots',
# 							'animal_image': 'deps/images/animal-4.png',
# 							'caption': 'Wildlife Nature',
# 							'paragraph': '"Lorem ipsum dolor sit amet, consectetur',
# 							'video': 'deps/videos/animal-video-4.mp4',
# 							'video_description': '"Lorem ipsum dolor sit amet, consectetur adipiscing elit'
# 					},
# 					{
# 							'bg_image': 'deps/images/bg-5.jpg',
# 							'animal_name': 'Red FOX',
# 							'animal_image': 'deps/images/animal-5.png',
# 							'caption': 'Wildlife Nature',
# 							'paragraph': 'Давно выяснено, что при оценке дизайна и композиции читаемый текст мешает',
# 							'video': 'deps/videos/animal-video-5.mp4',
# 							'video_description': 'Давно выяснено, что при оценке дизайна'
# 					},
# 					{
# 							'bg_image': 'deps/images/bg-6.jpg',
# 							'animal_name': 'Parrots',
# 							'animal_image': 'deps/images/animal-6.png',
# 							'caption': 'Wildlife Nature',
# 							'paragraph': '"Lorem ipsum dolor sit amet, consectetur',
# 							'video': 'deps/videos/animal-video-6.mp4',
# 							'video_description': '"Lorem ipsum dolor sit amet, consectetur adipiscing elit'
# 					},
# 					{
# 							'bg_image': 'deps/images/bg-7.jpg',
# 							'animal_name': 'Red FOX',
# 							'animal_image': 'deps/images/animal-7.png',
# 							'caption': 'Wildlife Nature',
# 							'paragraph': 'Давно выяснено, что при оценке дизайна и композиции читаемый текст мешает',
# 							'video': 'deps/videos/animal-video-7.mp4',
# 							'video_description': 'Давно выяснено, что при оценке дизайна'
# 					},
# 					{
# 							'bg_image': 'deps/images/bg-8.jpg',
# 							'animal_name': 'Parrots',
# 							'animal_image': 'deps/images/animal-8.png',
# 							'caption': 'Wildlife Nature',
# 							'paragraph': '"Lorem ipsum dolor sit amet, consectetur',
# 							'video': 'deps/videos/animal-video-8.mp4',
# 							'video_description': '"Lorem ipsum dolor sit amet, consectetur adipiscing elit'
# 					},
# 					{
# 							'bg_image': 'deps/images/bg-9.jpg',
# 							'animal_name': 'Parrots',
# 							'animal_image': 'deps/images/animal-9.png',
# 							'caption': 'Wildlife Nature',
# 							'paragraph': '"Lorem ipsum dolor sit amet, consectetur',
# 							'video': 'deps/videos/animal-video-9.mp4',
# 							'video_description': '"Lorem ipsum dolor sit amet, consectetur adipiscing elit'
# 					},
# 			]
# 		}
# 		return render(request, 'main/index.html', context=context)
	


class AboutView(View):
	def get(self, request):
		context = {
			'title': 'Home - О нас',
			'content': "О нас",
			'text_on_page': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."
		}
		return render(request, 'main/about.html', context=context)
	
	

class ContactView(View):
	def get(self, request):
		context = {
			'title': 'Home - Контакты',
			'content': "Контакты",
			'e_mail': "example@gmail.com",
			'phone': '+79155040000',
		}
		return render(request, 'main/contact.html', context=context)
	


class DroppView(View):
	def get(self, request):
		context = {
			'title': 'Home - Доставка',
			'content': "Доставка",
			'dropshipp': "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like)",
			'pay': "Оплата",
		}
		return render(request, 'main/drop-shipping.html', context=context)


# # Без классов 

# def index(request):
# 	return HttpResponse('Home page')


# def about(request):
# 	return HttpResponse('About page')