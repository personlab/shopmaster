# from datetime import timezone
from time import timezone
from email.mime import image

import re
from turtle import title
from urllib import request
from django.conf import settings
from django.db.models import CharField
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache

from django.shortcuts import render, get_object_or_404
from django.test import tag
from django.views import View
from django.core.paginator import EmptyPage, PageNotAnInteger

from django.db.models import F, Value
from django.db.models.functions import Concat
from itertools import chain

from django.http import Http404, JsonResponse
from pygments import highlight
import requests

from blog.forms import CommentForm, CommentRecentForm

from .models import Post, Hero, Featured, RecentPost, Tag, Comment

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchHeadline


import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from users.models import User, Wallet



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
				# Защита от ботов: проверка honeypot-поля
				if request.POST.get('honeypot'):
						return JsonResponse({
								"status": "error",
								"message": "❌ Bot detected!"
						}, status=400)
				
				# Получаем данные и обрезаем пробелы
				user_name = request.POST.get('user_name', '').strip()
				user_email = request.POST.get('user_email', '').strip()
				user_phone = request.POST.get('user_phone', '').strip()
				user_message = request.POST.get('user_message', '').strip()

				# Проверка на пустые поля
				if not all([user_name, user_email, user_phone, user_message]):
						return JsonResponse({
								"status": "error",
								"message": "❌ Все поля обязательны для заполнения!"
						}, status=400)

				# Валидация email
				if '@' not in user_email or '.' not in user_email.split('@')[-1]:
						return JsonResponse({
								"status": "error",
								"message": "❌ Введите корректный email"
						}, status=400)

				# Валидация телефона
				phone_regex = r'^(\+7|8)[\d\- ]{10,15}$'
				cleaned_phone = re.sub(r'[^\d]', '', user_phone)
				
				if not re.fullmatch(phone_regex, user_phone) or len(cleaned_phone) != 11:
						return JsonResponse({
								"status": "error",
								"message": "❌ Введите номер в формате +7XXX... или 8XXX... (11 цифр)"
						}, status=400)

				# Нормализация номера
				formatted_phone = '+7' + cleaned_phone[1:] if cleaned_phone.startswith('8') else '+' + cleaned_phone

				# Формируем сообщение для Telegram
				message = (
						f"GameTonApp. Новое сообщение со страницы Blog:\n"
						f"Имя: {user_name}\n"
						f"Email: {user_email}\n"
						f"Телефон: {formatted_phone}\n"
						f"Сообщение: {user_message}"
				)

				# Отправка в Telegram
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
				hero = cache.get('hero')
				if not hero:
						hero = Hero.objects.first()
						cache.set('hero', hero, 60*15)

				# Проверяем наличие записей в модели Post
				# posts = Post.objects.all() if Post.objects.exists() else []
				posts = cache.get('posts')
				if not posts:
						posts = Post.objects.filter(is_archived=False) if Post.objects.exists() else []
						cache.set('posts', posts, 60*15)

				popular_tags = cache.get('popular_tags')
				if not popular_tags:
						popular_tags = Tag.objects.all().order_by('-popularity_count')[:12] 
						cache.set('popular_tags', popular_tags, 60*15) # Кеш на 15 минут
						# Извлечение тегов/сортировка по популярности

				# Получить посты из таблицы Post
				post_posts = cache.get('post_posts')
				if not post_posts:
						post_posts = Post.objects.annotate(
								model_type=Value('Post', output_field=CharField())
						).values(
								'id', 'title', 'slug', 'content', 'image', 'created_at', 'reading_time', 'author_name', 'popularity_count', 'model_type'
						)
						cache.set('post_posts', post_posts, 60*15)

				# Получить посты из таблицы RecentPost
				recent_posts_one = cache.get('recent_posts_one')
				if not recent_posts_one:
						recent_posts_one= RecentPost.objects.annotate(
								model_type=Value('RecentPost', output_field=CharField())
						).values(
								'id', 'subtitle', 'title', 'slug', 'content', 'image', 'created_at', 'reading_time', 'author_name', 'popularity_count', 'model_type'
						)
						cache.set('recent_posts_one', recent_posts_one, 60*15)

				# Объединение QuerySets
				all_posts = sorted(
						chain(post_posts, recent_posts_one),
						key=lambda post: post['popularity_count'], 
						reverse=True
				)

				# Взять топ 5 популярных постов
				top_5_posts = all_posts[:5]

				# # Пагинация для RecentPost
				# recent_posts = RecentPost.objects.all()
				# paginator = Paginator(recent_posts, 1) # количество постов на странице

				recent_posts = RecentPost.objects.all().order_by('-created_at')  # Сортировка по дате создания
				paginator = Paginator(recent_posts, 1)  # количество постов на странице

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
				
				latest_comments = Comment.objects.select_related('post').order_by('-created_at')[:3] # Отображение 3 комментариев на странице блог в сайд баре


				context = {
						'title': 'GameTonApp - Game TON Tap-to-Earn',
						'description': 'Игры в телеграм, блокчейн TON, майнинг в телеграм, криптоигры, телеграм игры, заработок в телеграм',
						'posts': posts,
						'recent_posts_with_tags': recent_posts_with_tags,
						'hero': hero,
						'featured_items_with_tags': featured_items_with_tags,
						'top_5_posts': top_5_posts,
						'popular_tags': popular_tags,
						'paginator': paginator,
						'recent_posts': page_obj,
						'latest_comments': latest_comments,
				}

				return render(request, 'blog/post_list.html', context)



class TagPostsView(View):
		def post(self, request, tag_id=None):
				# # Защита от ботов: проверка honeypot-поля
				# if request.POST.get('honeypot'):
				# 		return JsonResponse({
				# 				"status": "error",
				# 				"message": "❌ Bot detected!"
				# 		}, status=400)
				
				# Получаем данные и обрезаем пробелы
				user_name = request.POST.get('user_name', '').strip()
				user_email = request.POST.get('user_email', '').strip()
				user_phone = request.POST.get('user_phone', '').strip()
				user_message = request.POST.get('user_message', '').strip()

				# Проверка на пустые поля
				if not all([user_name, user_email, user_phone, user_message]):
						return JsonResponse({
								"status": "error",
								"message": "❌ Все поля обязательны для заполнения!"
						}, status=400)

				# Валидация email
				if '@' not in user_email or '.' not in user_email.split('@')[-1]:
						return JsonResponse({
								"status": "error",
								"message": "❌ Введите корректный email"
						}, status=400)

				# Валидация телефона
				phone_regex = r'^(\+7|8)[\d\- ]{10,15}$'
				cleaned_phone = re.sub(r'[^\d]', '', user_phone)
				
				if not re.fullmatch(phone_regex, user_phone) or len(cleaned_phone) != 11:
						return JsonResponse({
								"status": "error",
								"message": "❌ Введите номер в формате +7XXX... или 8XXX... (11 цифр)"
						}, status=400)

				# Нормализация номера
				formatted_phone = '+7' + cleaned_phone[1:] if cleaned_phone.startswith('8') else '+' + cleaned_phone

				# Формируем сообщение для Telegram
				message = (
						f"GameTonApp. Новое сообщение со страницы Tags:\n"
						f"Имя: {user_name}\n"
						f"Email: {user_email}\n"
						f"Телефон: {formatted_phone}\n"
						f"Сообщение: {user_message}"
				)

				# Отправка в Telegram
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
		



		def get(self, request, tag_id):
				hero = Hero.objects.first()
				tags = get_object_or_404(Tag, id=tag_id)
				tags.popularity_count += 1
				tags.save()
				posts = tags.post.all() # Получаем все теги из основной модели Post
				recent_posts_with_tag = RecentPost.objects.filter(tags=tags) # Получаем посты с тегом из модели RecentPost

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
						'title': f'Посты с тегом {tags.name}',
						'posts': posts,
						'recent_posts_with_tag': recent_posts_with_tag,
						'tag': tags,
						'hero': hero,
						'top_5_posts': top_5_posts,
				}
				return render(request, 'blog/tag_posts.html', context=context)



class PostDetailView(View):
		def get(self, request, slug):
				hero = Hero.objects.first()
				tags = []
				recent_posts_with_tags = []
				form = None  # Изначально форма не определена

				# Проверка RecentPost
				post = RecentPost.objects.filter(slug=slug).first()
				if post:
						post.popularity_count += 1
						post.save()
						recent_posts_with_tags = [
								(recent_post, recent_post.tags.all())
								for recent_post in RecentPost.objects.prefetch_related('tags').all()
						]
				else:
						# Проверка Post
						post = Post.objects.filter(slug=slug).first()
						if post:
								post.popularity_count += 1
								post.save()
								tags = post.tags.all()  # Извлечение тегов из Post
								form = CommentForm(user=request.user)  # Создаем пустую форму только для Post
						else:
								raise Http404("No post matches the given query.")



				# Получить посты из таблицы Post
				post_posts = cache.get('post_posts')
				if not post_posts:
						post_posts = Post.objects.annotate(
								model_type=Value('Post', output_field=CharField())
						).values(
								'id', 'title', 'slug', 'content', 'image', 'created_at', 'reading_time', 'author_name', 'popularity_count', 'model_type'
						)
						cache.set('post_posts', post_posts, 60*15)

				# Получить посты из таблицы RecentPost
				recent_posts_one = cache.get('recent_posts_one')
				if not recent_posts_one:
						recent_posts_one= RecentPost.objects.annotate(
								model_type=Value('RecentPost', output_field=CharField())
						).values(
								'id', 'subtitle', 'title', 'slug', 'content', 'image', 'created_at', 'reading_time', 'author_name', 'popularity_count', 'model_type'
						)
						cache.set('recent_posts_one', recent_posts_one, 60*15)

				all_posts = sorted(
						chain(post_posts, recent_posts_one),
						key=lambda post: post['popularity_count'],
						reverse=True
				)

				top_5_posts = all_posts[:5]
				# Получить последние 3 комментария из всех постов
				latest_comments = Comment.objects.select_related('post').order_by('-created_at')[:3]
				comments = post.comments.all().order_by('-created_at') if isinstance(post, Post)  else []


				context = {
						'title': f'GameTonApp - {post.title}',
						'description': post.meta_description if post.meta_description else post.title,
						'post': post,
						'tags': tags,
						'hero': hero,
						'top_5_posts': top_5_posts,
						'comments': comments,
						'recent_posts_with_tags': recent_posts_with_tags,
						'form': form, # Передаем форму в контекст только в случае Post
						'latest_comments': latest_comments,
				}

				return render(request, 'blog/post_detail.html', context=context)

		
		def post(self, request, slug=None):
				# Защита от ботов: проверка honeypot-поля
				if request.POST.get('honeypot'):
						return JsonResponse({
								"status": "error",
								"message": "❌ Bot detected!"
						}, status=400)
				
				# Получаем данные и обрезаем пробелы
				if 'user_name' in request.POST:
						user_name = request.POST.get('user_name', '').strip()
						user_email = request.POST.get('user_email', '').strip()
						user_phone = request.POST.get('user_phone', '').strip()
						user_message = request.POST.get('user_message', '').strip()

						# Проверка на пустые поля
						if not all([user_name, user_email, user_phone, user_message]):
								return JsonResponse({
										"status": "error",
										"message": "❌ Все поля обязательны для заполнения!"
								}, status=400)

						# Валидация email
						if '@' not in user_email or '.' not in user_email.split('@')[-1]:
								return JsonResponse({
										"status": "error",
										"message": "❌ Введите корректный email"
								}, status=400)

						# Валидация телефона
						phone_regex = r'^(\+7|8)[\d\- ]{10,15}$'
						cleaned_phone = re.sub(r'[^\d]', '', user_phone)
						
						if not re.fullmatch(phone_regex, user_phone) or len(cleaned_phone) != 11:
								return JsonResponse({
										"status": "error",
										"message": "❌ Введите номер в формате +7XXX... или 8XXX... (11 цифр)"
								}, status=400)

						# Нормализация номера
						formatted_phone = '+7' + cleaned_phone[1:] if cleaned_phone.startswith('8') else '+' + cleaned_phone

						# Формируем сообщение для Telegram
						message = (
								f"GameTonApp. Новое сообщение со страницы Post:\n"
								f"Имя: {user_name}\n"
								f"Email: {user_email}\n"
								f"Телефон: {formatted_phone}\n"
								f"Сообщение: {user_message}"
						)

						# Отправка в Telegram
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
						
				
				hero = Hero.objects.first()

				if request.POST.get('type') == 'recent':
						try:
								recent_post = RecentPost.objects.get(slug=slug)
								selected_post = recent_post
						except RecentPost.DoesNotExist:
								recent_post = None
								selected_post = None
				else:
						post = get_object_or_404(Post, slug=slug)
						selected_post = post

				if selected_post is None:
						raise Http404("Пост не найден")

				if request.method == 'POST' and selected_post:
						form = CommentForm(request.POST, user=request.user)
						if form.is_valid():
								comment = form.save(commit=False)
								comment.post = selected_post

								# Сохраняем аватарку автора, если пользователь авторизован
								if request.user.is_authenticated:
										comment.author_image = request.user.image.url  # Предполагается, что у пользователя есть поле `image`
								else:
										comment.author_image = "{% static 'deps/images/baseavatar.jpg' %}"  # Используем аватарку по умолчанию для анонимных пользователей

								try:
										comment.save()

										# Если запрос AJAX, возвращаем JSON-ответ
										if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
												return JsonResponse({
														'success': True,
														'comment': {
																'text': comment.text,
																'author': comment.author,
																'author_image': comment.author_image,  # Добавляем URL аватарки в ответ
																'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M'),
														}
												})
										else:
												# Если это обычный POST-запрос, выполняем редирект
												return redirect('post_detail', slug=selected_post.slug) + f"?type=post"
								except Exception as e:
										print(f"Ошибка при сохранении комментария: {e}")
										if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
												return JsonResponse({'success': False, 'error': str(e)})
										else:
												# Обработка ошибки для обычного POST-запроса
												...
				elif selected_post:
						form = CommentForm(user=request.user)
				else:
						form = None

				# Получить посты из таблицы RecentPost
				recent_posts_one = RecentPost.objects.annotate(
						model_type=Value('RecentPost', output_field=CharField())
				).values(
						'id', 'subtitle', 'title', 'slug', 'content', 'image', 'created_at', 'reading_time', 'author_name', 'popularity_count', 'model_type'
				)

				# Получить посты из таблицы Post
				post_posts = Post.objects.annotate(
						model_type=Value('Post', output_field=CharField())
				).values(
						'id', 'title', 'slug', 'content', 'image', 'created_at', 'reading_time', 'author_name', 'popularity_count', 'model_type'
				)

				selected_post.popularity_count += 1
				selected_post.save()

				# Объединение QuerySets для всех постов
				all_posts = sorted(
						chain(post_posts, recent_posts_one),
						key=lambda post: post['popularity_count'],
						reverse=True
				)

				# Взять топ 5 популярных постов
				top_5_posts = all_posts[:5]

				tags = selected_post.tags.all()
				comments = selected_post.comments.all().order_by('-created_at') if selected_post else []

				context = {
						'hero': hero,
						'title': selected_post.title if selected_post else '',
						'description': post.meta_description if post.meta_description else post.title,
						'post': selected_post if selected_post else None,
						'recent_post': None,
						'tags': tags,
						'top_5_posts': top_5_posts,
						'comments': comments,
						'form': form if form else None,
				}

				return render(request, 'blog/post_detail.html', context=context)







class PostSearchView(View):
		def post(self, request, slug=None):
				# Защита от ботов: проверка honeypot-поля
				if request.POST.get('honeypot'):
						return JsonResponse({
								"status": "error",
								"message": "❌ Bot detected!"
						}, status=400)
				
				# Получаем данные и обрезаем пробелы
				user_name = request.POST.get('user_name', '').strip()
				user_email = request.POST.get('user_email', '').strip()
				user_phone = request.POST.get('user_phone', '').strip()
				user_message = request.POST.get('user_message', '').strip()

				# Проверка на пустые поля
				if not all([user_name, user_email, user_phone, user_message]):
						return JsonResponse({
								"status": "error",
								"message": "❌ Все поля обязательны для заполнения!"
						}, status=400)

				# Валидация email
				if '@' not in user_email or '.' not in user_email.split('@')[-1]:
						return JsonResponse({
								"status": "error",
								"message": "❌ Введите корректный email"
						}, status=400)

				# Валидация телефона
				phone_regex = r'^(\+7|8)[\d\- ]{10,15}$'
				cleaned_phone = re.sub(r'[^\d]', '', user_phone)
				
				if not re.fullmatch(phone_regex, user_phone) or len(cleaned_phone) != 11:
						return JsonResponse({
								"status": "error",
								"message": "❌ Введите номер в формате +7XXX... или 8XXX... (11 цифр)"
						}, status=400)

				# Нормализация номера
				formatted_phone = '+7' + cleaned_phone[1:] if cleaned_phone.startswith('8') else '+' + cleaned_phone

				# Формируем сообщение для Telegram
				message = (
						f"GameTonApp. Новое сообщение со страницы Search:\n"
						f"Имя: {user_name}\n"
						f"Email: {user_email}\n"
						f"Телефон: {formatted_phone}\n"
						f"Сообщение: {user_message}"
				)

				# Отправка в Telegram
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
				query = request.GET.get('q', '')  # Получаем запрос из параметра GET
				query = re.sub(r'[@#$%^&*()]', '', query)  # Очищаем запрос от специальных символов

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

				highlighted_posts = []

				if query:  # Проверяем, что запрос не пуст
						search_query = SearchQuery(query)

						# Поиск в обеих моделях
						posts_search = Post.objects.annotate(
								search=SearchVector('title', 'content')  # Создаем вектор поиска для Post
						).filter(search=search_query)

						recent_posts_search = RecentPost.objects.annotate(
								search=SearchVector('title', 'content')  # Создаем вектор поиска для RecentPost
						).filter(search=search_query)

						def highlight_text(text, query):
								highlight_style = "<span>{}</span>"
								pattern = re.compile(re.escape(query), re.IGNORECASE)  # Создаем регулярное выражение для поиска
								return pattern.sub(lambda m: highlight_style.format(m.group(0)), text)  # Заменяем найденные слова на выделенные

						for post in posts_search:
								highlighted_title = highlight_text(post.title, query)  # Выделяем заголовок
								highlighted_content = highlight_text(post.content, query)  # Выделяем контент
								highlighted_posts.append({
										'title': highlighted_title,
										'content': highlighted_content,
										'slug': post.slug,
								})

						for recent_post in recent_posts_search:
								highlighted_title = highlight_text(recent_post.title, query)  # Выделяем заголовок
								highlighted_content = highlight_text(recent_post.content, query)  # Выделяем контент
								highlighted_posts.append({
										'title': highlighted_title,
										'content': highlighted_content,
										'slug': recent_post.slug,
								})

				context = {
						'hero': hero,
						'title': f'GameTonApp - Результаты поиска по запросу {query}',
						'posts': highlighted_posts,
						'query': query,
						'top_5_posts': top_5_posts
				}

				return render(request, 'blog/search.html', context=context)
		




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
import json
import logging
from users.models import Wallet

logger = logging.getLogger('ton-connect')

@csrf_exempt
@require_POST
def ton_auth(request):
		try:
				data = json.loads(request.body)
				wallet_address = data.get('wallet_address')
				tg_user = data.get('telegram_data', {})
				
				if not wallet_address:
						return JsonResponse({"success": False, "error": "Wallet address required"}, status=400)
				
				wallet, created = Wallet.objects.update_or_create(
						address=wallet_address,
						defaults={
								'telegram_id': tg_user.get('id'),
								'telegram_username': tg_user.get('username'),
								'telegram_first_name': tg_user.get('first_name'),
								'telegram_last_name': tg_user.get('last_name'),
								'telegram_photo_url': tg_user.get('photo_url'),
						}
				)
				
				return JsonResponse({
						"success": True,
						"created": created,
						"wallet": {
								"address": wallet.address,
								"username": wallet.telegram_username,
								"first_name": wallet.telegram_first_name,
								"last_name": wallet.telegram_last_name,
								"photo_url": wallet.telegram_photo_url,
						}
				})
				
		except Exception as e:
				logger.error(f"TON auth error: {str(e)}", exc_info=True)
				return JsonResponse({"success": False, "error": str(e)}, status=400)



logger = logging.getLogger('wallet')

@csrf_exempt
@require_POST
def wallet_info(request):
		"""
		Обработчик для сохранения информации о кошельке
		"""
		try:
				# Логирование сырых данных
				raw_data = request.body.decode('utf-8')
				logger.debug(f"Raw request data: {raw_data}")
				
				# Парсинг JSON
				try:
						data = json.loads(raw_data)
				except json.JSONDecodeError as e:
						logger.error(f"JSON decode error: {str(e)}")
						return JsonResponse({
								"success": False,
								"error": "Invalid JSON format"
						}, status=400)
				
				# Валидация обязательных полей
				if not data.get('address'):
						logger.error("Wallet address is missing")
						return JsonResponse({
								"success": False,
								"error": "Wallet address is required"
						}, status=400)
				
				# Подготовка данных для сохранения
				telegram_data = data.get('telegram_data') or {}
				wallet_data = {
						'telegram_id': telegram_data.get('id'),
						'telegram_username': telegram_data.get('username'),
						'telegram_first_name': telegram_data.get('first_name'),
						'telegram_last_name': telegram_data.get('last_name'),
						'telegram_photo_url': telegram_data.get('photo_url'),
				}
				
				# Очистка от None значений
				wallet_data = {k: v for k, v in wallet_data.items() if v is not None}
				
				logger.debug(f"Prepared wallet data: {wallet_data}")
				
				# Создаем или обновляем запись кошелька
				wallet, created = Wallet.objects.update_or_create(
						address=data['address'],
						defaults=wallet_data
				)
				
				logger.info(f"Wallet {'created' if created else 'updated'}: {wallet.address}")
				
				# Формируем ответ
				response_data = {
						"success": True,
						"created": created,
						"wallet": {
								"address": wallet.address,
								"telegram_username": wallet.telegram_username,
								"telegram_first_name": wallet.telegram_first_name,
								"telegram_last_name": wallet.telegram_last_name,
								"telegram_photo_url": wallet.telegram_photo_url,
						}
				}
				
				return JsonResponse(response_data)
				
		except Exception as e:
				logger.exception("Unexpected error in wallet_info")
				return JsonResponse({
						"success": False,
						"error": "Internal server error"
				}, status=500)
		


