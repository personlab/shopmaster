from itertools import product
from django.http import request
from django.shortcuts import render, get_object_or_404
from django.views import View

from goods.models import Products


class CatalogView(View):
		def get(self, request):
			goods = Products.objects.all()
			context = {
							"title": "Home - Каталог",
							"goods": goods,
					}
			return render(request, "goods/catalog.html", context=context)


class ProductView(View):
		def get(self, request, product_slug):
				product = get_object_or_404(Products, slug=product_slug)
				context = {
					'product': product
				}
				return render(request, "goods/product.html", context=context)
