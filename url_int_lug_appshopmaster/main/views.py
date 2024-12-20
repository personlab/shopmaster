from turtle import title
from django.http import HttpResponse
from django.shortcuts import render
from django.template import context
import requests

from goods import views
from goods.models import Categories
from main.models import Slide
from django.conf import settings
from django.http import JsonResponse
from blog.models import Hero

#  С применением классов
from django.views import View


class SendMessageTelegramView:
		def send_message(self, message):
				bot_token = settings.TELEGRAM_BOT_TOKEN
				chat_id = settings.TELEGRAM_CHAT_ID
				url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

				payload = {
						'chat_id': chat_id,
						'text': message,
				}

				requests.post(url, data=payload)


class IndexView(View):
		def get(self, request):
			slides = Slide.objects.all() # извлекаем все слайды из базы данных
			context = {
				'title': 'TonGameApp - Главная',
				'slides': slides
			}
			return render(request, 'main/index.html', context=context)
		

class AboutView(View):
	def get(self, request):
		context = {
			'title': 'Home - О нас',
			'content': "О нас",
			'text_on_page': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."
		}
		return render(request, 'main/about.html', context=context)
	
	

class ContactView(View):
	def post(self, request):
		user_name = request.POST.get('user_name')
		user_email = request.POST.get('user_email')
		user_phone = request.POST.get('email_phone')
		user_message = request.POST.get('user_message')

		message = f"Новое сообщение от {user_name}:\nEmail: {user_email}\nТелефон: {user_phone}\nСообщение: {user_message}"

		# Создаем экземпляр класса SendMessageTelegramView и отправляем сообщение
		telegram_sender = SendMessageTelegramView()
		telegram_sender.send_message(message)

		return JsonResponse({"status": "success", "message": "✅ Сообщение отправлено"})
			
	def get(self, request):
		hero = Hero.objects.first()
		context = {
			'title': 'Home - Контакты',
			'content': "Контакты",
			'e_mail': "example@gmail.com",
			'phone': '+79155040000',
			'hero': hero,
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