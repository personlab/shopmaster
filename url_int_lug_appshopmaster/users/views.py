from django.shortcuts import render
from django.views import View
from urllib import request
from django.conf import settings
from django.http import Http404, JsonResponse
import requests
from django.db.models import F, CharField, Value
from itertools import chain

from blog.models import Hero, Post, RecentPost


# Create your views here.


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


class LoginViews(View):
			
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

				# Получить посты из таблицы Post
				post_posts = Post.objects.annotate(
						model_type=Value('Post', output_field=CharField())
				).values(
						'id', 'title', 'slug', 'content', 'image', 'created_at', 'reading_time', 'author_name', 'popularity_count', 'model_type'
				)

				# Получить посты из таблицы RecentPost
				recent_posts_one = RecentPost.objects.annotate(
						model_type=Value('RecentPost', output_field=CharField())
				).values(
						'id', 'subtitle', 'title', 'slug', 'content', 'image', 'created_at', 'reading_time', 'author_name', 'popularity_count', 'model_type'
				)

				# Объединение QuerySets
				all_posts = sorted(
						chain(post_posts, recent_posts_one),
						key=lambda post: post['popularity_count'], 
						reverse=True
				)

				# Взять топ 5 популярных постов
				top_5_posts = all_posts[:5]

		
				context = {
						'title': 'TonGameApp - Авторизация|Регистрация',
						'hero': hero,
						'top_5_posts': top_5_posts,
				}

				return render(request, 'users/log_reg.html', context=context)
		

		
class RegistrationView(View):
			
			def get(self, request):
				context = {
						'title': 'TonGameApp - Авторизация|Регистрация',
				}

				return render(request, 'users/log_reg.html', context=context)
			


class ProfileView(View):
		
		def get(self, request):
				context = {
					'title': 'TonGameApp - Профиль',
				}

				return render(request, 'users/profile.html', context=context)
		

class LogoutView(View):
		
		def get(self, request):
				context = {
					'title': 'TonGameApp - Профиль',
				}

				return render(request, 'users/profile.html', context=context)