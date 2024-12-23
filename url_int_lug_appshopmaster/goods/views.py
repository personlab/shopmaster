from itertools import product
from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse, request
from django.shortcuts import get_list_or_404, render, get_object_or_404
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

			page = request.GET.get('page', 1)

			if category_slug == 'all':
					goods = Products.objects.all()
			else:
					goods = get_list_or_404(
						Products.objects.filter(category__slug=category_slug)
						) # get_list_or_404 если ожидаем список
					
			paginator = Paginator(goods, 3)
			current_page = paginator.page(int(page))

			context = {
							"title": "Home - Каталог",
							"hero": hero,
							"goods": current_page,
							"slug_url": category_slug,
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
						product = get_object_or_404(Products, id=product_id) # get_object_or_404 ошибка если нет объекта
				else:
						product = get_object_or_404(Products, slug=product_slug)
				context = {
					'product': product
				}
				return render(request, "goods/product.html", context=context)
