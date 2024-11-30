from email.mime import image
from turtle import title
from urllib import request
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import Post, Hero, Featured

class PostsView(View):
		def get(self, request):
				hero = Hero.objects.first() # Получаем первого героя на странице post
				posts = Post.objects.all() # Извлекаем все записи блога
				featured_items = Featured.objects.order_by('-created_at')[:5] # извлекаем последние пять постов в разделе избранные
				context = {
						'title': 'TonGameApp - Блог',
						'posts': posts,
						'hero': hero,
						'featured_items': featured_items
				}
				return render(request, 'blog/post_list.html', context=context)


class PostDetailView(View):
		def get(self, request, slug):
				post = get_object_or_404(Post, slug=slug)
				context = {
						'title': post.title,
						'post': post
				}
				return render(request, 'blog/post_detail.html', context=context)


# class FeaturedView(View):
# 		def get(self, request):
# 				featured_items = Featured.objects.all()
# 				context = {
# 						'featured_items': featured_items,
# 				}
# 				return render(request, 'blog/post_list.html', context=context)
