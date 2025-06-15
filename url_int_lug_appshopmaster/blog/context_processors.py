from .models import Comment

def latest_comments(request):
		return {
				'latest_comments': Comment.objects.select_related('post').order_by('-created_at')[:3]
		}


def version(request):
		return {'APP_VERSION': '3.22.6'}