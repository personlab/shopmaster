from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import Post

class PostsView(View):
		def get(self, request):
				posts = Post.objects.all()  # Извлекаем все записи блога
				context = {
						'title': 'TonGameApp - Блог',
						'posts': posts
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
