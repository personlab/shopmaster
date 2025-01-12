from django.urls import path
from blog.views import PostsView, PostDetailView, TagPostsView, PostSearchView

app_name = 'blog'

urlpatterns = [
		path('search/', PostSearchView.as_view(), name='search'),
		path('', PostsView.as_view(), name='post_list'),
		path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
		path('tags/<int:tag_id>/', TagPostsView.as_view(), name='tag_posts'),
]