from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories


#  С применением классов
from django.views import View

class IndexView(View) :

	categories = Categories.objects.all()

	def get(self, request):
		context = {
			'title': 'Home - главная',
			'content': 'Магазин мебели HOME',
			'categories': self.categories
		}
		return render(request, 'main/index.html', context=context)
	


class AboutView(View):
	def get(self, request):
		context = {
			'title': 'Home - О нас',
			'content': "О нас",
			'text_on_page': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."
		}
		return render(request, 'main/about.html', context=context)
	
	

class ContactView(View):
	def get(self, request):
		context = {
			'title': 'Home - Контакты',
			'content': "Контакты",
			'e_mail': "example@gmail.com",
			'phone': '+79155040000',
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

# Без классов 

# def index(request):
# 	return HttpResponse('Home page')


# def about(request):
# 	return HttpResponse('About page')