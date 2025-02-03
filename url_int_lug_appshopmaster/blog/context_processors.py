from .models import Comment

def latest_comments(request):
		return {
				'latest_comments': Comment.objects.select_related('post').order_by('-created_at')[:3]
		}