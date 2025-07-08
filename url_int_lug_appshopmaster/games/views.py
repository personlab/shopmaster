from django.shortcuts import render

import re
from turtle import title
from django.http import HttpResponse
from django.shortcuts import render
from django.template import context
import requests

from django.db.models import F, Value
from django.db.models.functions import Concat
from itertools import chain
from django.db.models import CharField

from goods import views
from goods.models import Categories
from main.models import Slide
from django.conf import settings
from django.http import JsonResponse
from blog.models import Hero
from .models import Game

# С применением классов
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


class GamesView(View):
	def post(self, request):
			user_name = request.POST.get('user_name')
			user_email = request.POST.get('user_email')
			user_phone = request.POST.get('user_phone') # Обратите внимание на имя поля!
			user_message = request.POST.get('user_message')

			# Валидация формата телефона
			phone_regex = r'^(\+7|8)\d{10}$'
			cleaned_phone = re.sub(r'[^\d]', '', user_phone)  # Удаляем все не-цифры
			
			if not re.fullmatch(phone_regex, user_phone) or len(cleaned_phone) != 11:
					return JsonResponse({
							"status": "error",
							"message": "❌ Введите номер в формате +7XXX... или 8XXX... (11 цифр)"
					}, status=400)

			# Нормализация номера
			if cleaned_phone.startswith('8'):
					formatted_phone = '+7' + cleaned_phone[1:]
			else:
					formatted_phone = '+' + cleaned_phone

			message = f"GameTonApp. Новое сообщение от {user_name}:\nEmail: {user_email}\nТелефон: {formatted_phone}\nСообщение: {user_message}"

			try:
					telegram_sender = SendMessageTelegramView()
					telegram_sender.send_message(message)
					return JsonResponse({
							"status": "success", 
							"message": "✅ Сообщение отправлено"
					})
			except Exception as e:
					return JsonResponse({
							"status": "error",
							"message": f"❌ Ошибка отправки: {str(e)}"
					}, status=500)
	
			
	def get(self, request):

		hero = Hero.objects.first()
		games = Game.objects.filter(is_active=True).order_by('rank')
		context = {
			'title': "GameTonApp - Web3-игры на блокчейне TON в телеграм",
			'description': 'Открой мир увлекательных игр в Telegram на блокчейне TON! GameTonApp — это каталог Web3-игр с децентрализованными возможностями, где каждый найдёт игру по душе.',
			'keywords': "Web3-игры, TON-игры, Telegram-игры, блокчейн TON, децентрализованные игры, криптоигры, GameTonApp",
			'games': games,
			'hero': hero,
		}
		return render(request, 'games/games.html', context=context)
