from django.urls import path
from blog.views import PostsView, PostDetailView, TagPostsView

app_name = 'blog'

urlpatterns = [
		path('', PostsView.as_view(), name='post_list'),
		path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
		# path('recent-post/<slug:slug>/', RecentPostDetailView.as_view(), name='recent_post_detail'),
		path('tags/<int:tag_id>/', TagPostsView.as_view(), name='tag_posts'),
]