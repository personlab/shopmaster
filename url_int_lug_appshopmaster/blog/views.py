from email.mime import image
from turtle import title
from urllib import request
from django.conf import settings
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.test import tag
from django.views import View

from django.http import Http404, JsonResponse
import requests

from .models import Post, Hero, Featured, RecentPost, Tag

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


class PostsView(View):
		
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

				# Проверяем наличие записей в модели Post
				posts = Post.objects.all() if Post.objects.exists() else []

				# Проверяем наличие записей в модели RecentPost
				recent_posts_with_tags = []
				if RecentPost.objects.exists():
						recent_posts = RecentPost.objects.all()
						for recent_post in recent_posts:
								tags = recent_post.tags.all()  # Получаем теги для каждого поста
								recent_posts_with_tags.append((recent_post, tags))
				else:
						recent_posts = []

				# Проверяем наличие записей в Featured
				featured_items_with_tags = []
				if Featured.objects.exists():
						featured_items = Featured.objects.order_by('-created_at')[:5]
						for item in featured_items:
								post = item.post  # Проверяем есть ли связанный пост
								tags = post.tags.all() if post else []
								featured_items_with_tags.append((item, tags))

				context = {
						'title': 'TonGameApp - Блог',
						'posts': posts,
						'recent_posts_with_tags': recent_posts_with_tags,
						'hero': hero,
						'featured_items_with_tags': featured_items_with_tags,
				}

				return render(request, 'blog/post_list.html', context=context)


		

class TagPostsView(View):
		def post(self, request, tag_id=None):
				user_name = request.POST.get('user_name')
				user_email = request.POST.get('user_email')
				user_phone = request.POST.get('email_phone')
				user_message = request.POST.get('user_message')

				message = f"Новое сообщение от {user_name}:\nEmail: {user_email}\nТелефон: {user_phone}\nСообщение: {user_message}"

				# Создаем экземпляр класса SendMessageTelegramView и отправляем сообщение
				telegram_sender = SendMessageTelegramView()
				telegram_sender.send_message(message)

				return JsonResponse({"status": "success", "message": "✅ Сообщение отправлено"})

		def get(self, request, tag_id):
				hero = Hero.objects.first()
				tags = get_object_or_404(Tag, id=tag_id)
				posts = tags.post.all()
				context = {
						'title': f'Посты с тегом {tags.name}',
						'posts': posts,
						'tag': tags,
						'hero': hero,
				}
				return render(request, 'blog/tag_posts.html', context=context)


class PostDetailView(View):
		def post(self, request, slug=None):
				user_name = request.POST.get('user_name')
				user_email = request.POST.get('user_email')
				user_phone = request.POST.get('email_phone')
				user_message = request.POST.get('user_message')

				message = f"Новое сообщение от {user_name}:\nEmail: {user_email}\nТелефон: {user_phone}\nСообщение: {user_message}"

				# Создаем экземпляр класса SendMessageTelegramView и отправляем сообщение
				telegram_sender = SendMessageTelegramView()
				telegram_sender.send_message(message)

				return JsonResponse({"status": "success", "message": "✅ Сообщение отправлено"})

		def get(self, request, slug):
				hero = Hero.objects.first()
				post = None
				tags = []
				recent_posts_with_tags = []

				# Проверим сначала RecentPost
				if RecentPost.objects.filter(slug=slug).exists():
						post = get_object_or_404(RecentPost, slug=slug)
						recent_posts = RecentPost.objects.all()
						for recent_post in recent_posts:
								recent_tags = recent_post.tags.all()  # Получаем теги для каждого recent_post
								recent_posts_with_tags.append((recent_post, recent_tags))
				# Проверим в модели Post
				elif Post.objects.filter(slug=slug).exists():
						post = get_object_or_404(Post, slug=slug)
						tags = post.tags.all()
				# Если нигде не найдено
				else:
						raise Http404("No post matches the given query.")

				context = {
						'title': post.title,
						'post': post,
						'tags': tags,
						'hero': hero,
						'recent_posts_with_tags': recent_posts_with_tags, # Добавляем recent_posts_with_tags
				}

				return render(request, 'blog/post_detail.html', context=context)
