from email import contentmanager
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
from blog.models import Hero, Post, RecentPost

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


class IndexView(View):
		def get(self, request):
			slides = Slide.objects.all() # извлекаем все слайды из базы данных
			context = {
				'title': 'GameTonApp - Игры в телеграм',
				'description': 'игры в Telegram, Tap-to-Earn, блокчейн TON, майнинг в Telegram, криптоигры, Telegram игры, заработок в Telegram',
				'slides': slides
			}
			return render(request, 'index.html', context=context)
		

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

		hero = Hero.objects.first()
		context = {
			'title': 'GameTonApp - Контакты',
			'content': "Контакты",
			'e_mail': "baragin@yahoo.com",
			'phone': '+79155047791',
			'hero': hero,
			'top_5_posts': top_5_posts,
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
	

class YandexView(View):
	def get(self, request):
		content = """
		<html>
				<head>
						<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
				</head>
				<body>Verification: 889db48169eb8d68</body>
		</html>
		"""
		return HttpResponse(content, content_type='text/html')
	

class GoogleView(View):
	def get(self, request):
		content = """
		google-site-verification: googleed002019e2c6036a.html
		"""
		return HttpResponse(content, content_type='text/html')
	

class RobotsView(View):
	def get(self, request):
		content = """
			User-agent: *
			Disallow:
			Sitemap: https://gameton.app/sitemap.xml
		"""
		return HttpResponse(content, content_type='text/txt')
	


class SitemapView(View):
	def get(self, request):
		content = """
			<urlset
			xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
			xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
			xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
						http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
						<!-- created with Free Online Sitemap Generator www.xml-sitemaps.com -->

							<url>
								<loc>https://gameton.app/</loc>
								<lastmod>2025-03-09T17:41:52+00:00</lastmod>
								<priority>1.00</priority>
							</url>
								<url>
									<loc>https://gameton.app/blog/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.80</priority>
								</url>
								<url>
									<loc>https://gameton.app/contact/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.80</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/city-holder/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.80</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/city-holder-game/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.80</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/bump/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.80</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/tiny-verse/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.80</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/igry-v-telegram/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.80</priority>
								</url>
								<url>
									<loc>https://gameton.app/user/login/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/trumps-empire/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/tonkeeper/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/kitty-verse/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/welcome-to-whale/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/tags/1/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/tags/9/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/tags/7/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/tags/8/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/tags/6/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/tags/2/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/tags/5/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/tags/3/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/aqua-genesis-nfts/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/?page=1</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/?page=2</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/?page=7</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/user/registration/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.64</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/mmpro-group/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.51</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/tinyverse/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.51</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/trumpe/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.51</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/whale-casino/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.51</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/kittyverse/</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.51</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/?page=3</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.51</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/?page=6</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.51</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/?page=4</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.41</priority>
								</url>
								<url>
									<loc>https://gameton.app/blog/?page=5</loc>
									<lastmod>2025-03-09T17:41:52+00:00</lastmod>
									<priority>0.41</priority>
								</url>

						</urlset>
		"""
		return HttpResponse(content, content_type='text/xml')



def custom_404(request, exception=None):
		return render(request, 'main/404.html', status=404)


def custom_500(request):
		return render(request, 'main/500.html', status=500)
