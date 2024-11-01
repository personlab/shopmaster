from django.http import request
from django.shortcuts import render
from django.views import View

class CatalogView(View):
	def get(self, request):
		context = {
			'title': 'Home - главная',
			'content': 'Магазин мебели HOME'
		}
		return render(request, 'goods/catalog.html')
	


class ProductView(View):
	def get(self, request):
		context = {
			'title': 'tyu',
			'content': 'ghjhjh'
		}
		return render(request, 'goods/product.html')
