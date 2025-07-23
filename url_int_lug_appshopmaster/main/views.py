from email import contentmanager
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
from blog.models import Hero, Post, RecentPost

from django.views.decorators.csrf import csrf_exempt

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
				'description': 'game ton, игры в телеграм, BUMP, CITY Holder Game, Tiny Verse, Dropee, Trump\'s Empire, TONxDAO',
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
						f"GameTonApp. Новое сообщение со страницы Contact:\n"
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
			'description': 'Есть вопросы? Напишите нам',
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


@csrf_exempt
def ton_manifest(request):
		manifest = {
				"url": "https://gameton.app/blog/",
				"name": "GameTonApp",
				"iconUrl": "https://gameton.app/static/deps/favicon/apple-touch-icon.png",
		}
		return JsonResponse(manifest)
	

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
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>1.00</priority>
							</url>
							<url>
							<loc>https://gameton.app/user/login/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.80</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.80</priority>
							</url>
							<url>
							<loc>https://gameton.app/games/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.80</priority>
							</url>
							<url>
							<loc>https://gameton.app/contact/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.80</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/droppe-razbor-predstoyashego-listinga-i-stoit-li-uchastvovat-v-snimke-31-maya/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.80</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/antarctic-wallet-tvoj-nadezhnyj-kriptokoshelek-s-oplatoj-cherez-sbp/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.80</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/city-holder/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.80</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/trumps-empire/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.80</priority>
							</url>
							<url>
							<loc>https://gameton.app/user/registration/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/user/password_reset_form/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/ton-na-rynke-denezhnyh-perevodov-konec-western-union/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/optimizaciya-ton-kak-set-uskoryaetsya-masshtabiruetsya-i-gotovitsya-k-budushemu/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/ton-myortv/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/TON-k-2027-godu-smozhet-li-blokcheyn-Telegram-dobitsya-massovogo-vnedreniya/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/ton-vs-solana-gde-luchshe-igrat-v-2025-godu/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/web3-igry-pochemu-play-to-earn-provalilsya-i-chto-pridet-emu-na-smenu/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/kriptorynok-pered-altsezonom-kakie-monety-skupayut-investory/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/mexc-raj-dlya-teh-kto-verit-chto-internet-dengi-eto-vseryoz/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/toncoin-tokenomika-inflyaciya-szhiganie-i-ekonomika-ekosistemy/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/blockchaincom-vstrechaet-ton-integraciya-kotoraya-imeet-znachenie/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/tonkeeper/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/unikalnye-osobennosti-ton-i-chem-on-vydelyaetsya/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/zolotaya-viza-oae-cherez-ton-razbor-skandalnoj-iniciativy/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/stejking-ton-put-k-passivnomu-dohodu-i-setevoj-bezopasnosti/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/tags/7/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/tags/10/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/tags/1/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/tags/5/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/tags/6/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/tags/3/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/tags/2/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/tags/4/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/tags/9/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/tags/8/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/?page=1</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/?page=2</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/?page=3</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
							</url>
							<url>
							<loc>https://gameton.app/blog/dropee/</loc>
							<lastmod>2025-07-18T23:29:33+00:00</lastmod>
							<priority>0.64</priority>
					</url>


				</urlset>
		"""
		return HttpResponse(content, content_type='text/xml')



def custom_404(request, exception=None):
		return render(request, 'main/404.html', status=404)


def custom_500(request):
		return render(request, 'main/500.html', status=500)
