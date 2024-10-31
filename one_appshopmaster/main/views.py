from django.http import HttpResponse
from django.shortcuts import render


#  С применением классов
from django.views import View

class IndexView(View) :
	def get(self, request):
		context = {
			'file': 'Home',
			'content': 'Главная страница - HOME',
			'list': ['first', 'second'],
			'dict': {'first': 1},
			'is_authenticated': False
		}
		return render(request, 'main/index.html', context)


class AboutView(View):
	def get(self, request):
		return HttpResponse('About page')

# Без классов 

# def index(request):
# 	return HttpResponse('Home page')


# def about(request):
# 	return HttpResponse('About page')