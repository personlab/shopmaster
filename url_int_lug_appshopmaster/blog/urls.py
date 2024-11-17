from django.urls import path
from blog.views import PostsView, PostDetailView

app_name = 'blog'

urlpatterns = [
		path('', PostsView.as_view(), name='post_list'),
		path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]