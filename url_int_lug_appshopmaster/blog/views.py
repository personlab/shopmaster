from email.mime import image
from turtle import title
from urllib import request
from django.conf import settings
from django.db.models import CharField
from django.shortcuts import render
from django.core.paginator import Paginator

from django.shortcuts import render, get_object_or_404
from django.test import tag
from django.views import View
from django.core.paginator import EmptyPage, PageNotAnInteger

from django.db.models import F, Value
from django.db.models.functions import Concat
from itertools import chain

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
				popular_tags = Tag.objects.all().order_by('-popularity_count')[:12] # Извлечение тегов/сортировка по популярности

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

				# Пагинация для RecentPost
				recent_posts = RecentPost.objects.all()
				paginator = Paginator(recent_posts, 2) # количество постов на странице

				# Получение номера страницы из GET-параметров
				page_number = request.GET.get('page', 1)

				try:
						page_number = int(page_number)
				except (ValueError, TypeError):
						page_number = 1 # Устанавливаем на 1 при ошибке преобразования

				try:
						page_obj = paginator.page(int(page_number)) # Работаем со страницей
				except EmptyPage:
						# Если номер страницы недопустим, показываем первую страницу
						page_obj = paginator.page(1)

				recent_posts_with_tags = [
						(recent_post, recent_post.tags.all()) for recent_post in page_obj
				]

				featured_items_with_tags = []
				if Featured.objects.exists():
						featured_items = Featured.objects.order_by('-created_at')[:5]
						for item in featured_items:
								post = item.post
								tags = post.tags.all() if post else []
								featured_items_with_tags.append((item, tags))


				context = {
						'title': 'TonGameApp - Блог',
						'posts': posts,
						'recent_posts_with_tags': recent_posts_with_tags,
						'hero': hero,
						'featured_items_with_tags': featured_items_with_tags,
						'top_5_posts': top_5_posts,
						'popular_tags': popular_tags,
						'paginator': paginator,
						'recent_posts': page_obj
				}

				return render(request, 'blog/post_list.html', context)



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
				tags.popularity_count += 1
				tags.save()
				posts = tags.post.all() # Получаем все теги из основной модели Post
				recent_posts_with_tag = RecentPost.objects.filter(tags=tags) # Получаем посты с тегом из модели RecentPost
				context = {
						'title': f'Посты с тегом {tags.name}',
						'posts': posts,
						'recent_posts_with_tag': recent_posts_with_tag,
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

				# Проверка RecentPost
				if RecentPost.objects.filter(slug=slug).exists():
						post = get_object_or_404(RecentPost, slug=slug)
						post.popularity_count += 1
						post.save()
						recent_posts_with_tags = [
								(recent_post, recent_post.tags.all())
				for recent_post in RecentPost.objects.prefetch_related('tags')  # Prefetch tags
										]
				# Проверка Post
				elif Post.objects.filter(slug=slug).exists():
						post = get_object_or_404(Post, slug=slug)
						post.popularity_count += 1
						post.save()
						tags = post.tags.all() # Извлечение тегов из Post
				else:
						raise Http404("No post matches the given query.")

				context = {
						'title': post.title,
						'post': post,
						'tags': tags,
						'hero': hero,
						'top_5_posts': top_5_posts,
						'recent_posts_with_tags': recent_posts_with_tags,
				}

				return render(request, 'blog/post_detail.html', context=context)


