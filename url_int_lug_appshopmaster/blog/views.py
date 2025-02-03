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
				# posts = Post.objects.all() if Post.objects.exists() else []
				posts = Post.objects.filter(is_archived=False) if Post.objects.exists() else []
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
				paginator = Paginator(recent_posts, 1) # количество постов на странице

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
				
				latest_comments = Comment.objects.select_related('post').order_by('-created_at')[:3]


				context = {
						'title': 'TonGameApp - Блог',
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

				all_posts = sorted(
						chain(post_posts, recent_posts_one),
						key=lambda post: post['popularity_count'],
						reverse=True
				)

				top_5_posts = all_posts[:5]
				# Получить последние 3 комментария из всех постов
				latest_comments = Comment.objects.select_related('post').order_by('-created_at')[:3]


				context = {
						'title': post.title,
						'post': post,
						'tags': tags,
						'hero': hero,
						'top_5_posts': top_5_posts,
						'recent_posts_with_tags': recent_posts_with_tags,
						'form': form, # Передаем форму в контекст только в случае Post
						'latest_comments': latest_comments,
				}

				return render(request, 'blog/post_detail.html', context=context)

		
		def post(self, request, slug=None):
				# Обработка формы отправки сообщения в Telegram
				if 'user_name' in request.POST:
						user_name = request.POST.get('user_name')
						user_email = request.POST.get('user_email')
						user_phone = request.POST.get('user_phone')
						user_message = request.POST.get('user_message')

						message = f"TonGameApp. Новое сообщение от {user_name}:\nEmail: {user_email}\nТелефон: {user_phone}\nСообщение: {user_message}"

						# Создаем экземпляр класса SendMessageTelegramView и отправляем сообщение
						telegram_sender = SendMessageTelegramView()
						telegram_sender.send_message(message)

						return JsonResponse({"status": "success", "message": "✅ Сообщение отправлено"})
				
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
										comment.author_image = "{% static 'deps/images/default-avatar.png' %}"  # Используем аватарку по умолчанию для анонимных пользователей

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
				comments = selected_post.comments.all() if selected_post else []

				context = {
						'hero': hero,
						'title': selected_post.title if selected_post else '',
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
				query = request.GET.get('q', '')  # Получаем запрос из параметра GET
				# posts = Post.objects.all()


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

				if query:  # Проверяем, что запрос не пуст
						search_query = SearchQuery(query)

						# Поиск в обеих моделях
						posts_search = Post.objects.annotate(
								search=SearchVector('title', 'content')  # Создаем вектор поиска для Post
						).filter(search=search_query)

						recent_posts_search = RecentPost.objects.annotate(
								search=SearchVector('title', 'content')  # Создаем вектор поиска для RecentPost
						).filter(search=search_query)

						highlighted_posts = []

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

				else:
						highlighted_posts = []  # Пустой список, если запрос пуст

				context = {
						'hero': hero,
						'title': 'Результаты поиска',
						'posts': highlighted_posts,
						'query': query,
						'top_5_posts': top_5_posts
				}

				return render(request, 'blog/search.html', context=context)



