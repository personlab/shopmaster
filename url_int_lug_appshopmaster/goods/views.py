from itertools import product
from django.conf import settings
from django.http import JsonResponse, request
from django.shortcuts import render, get_object_or_404
from django.views import View
import requests

from goods.models import Products
from blog.models import Hero


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


class CatalogView(View):
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

		def get(self, request, category_slug):
			hero = Hero.objects.first()

			if category_slug == 'all':
					goods = Products.objects.all()
			else:
					goods = Products.objects.filter(category__slug=category_slug)

			context = {
							"title": "Home - Каталог",
							"goods": goods,
							"hero": hero,
					}
			return render(request, "goods/catalog.html", context=context)


class ProductView(View):
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
		def get(self, request, product_slug=False, product_id=False):
				
				if product_id:
						product = get_object_or_404(Products, id=product_id)
				else:
						product = get_object_or_404(Products, slug=product_slug)
				context = {
					'product': product
				}
				return render(request, "goods/product.html", context=context)
