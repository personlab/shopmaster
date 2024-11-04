from django.http import request
from django.shortcuts import render
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
    def get(self, request):
        context = {"title": "tyu", "content": "ghjhjh"}
        return render(request, "goods/product.html")
