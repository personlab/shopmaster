from django.shortcuts import render
from .models import Comment
from django.conf import settings

def latest_comments(request):
		return {
				'latest_comments': Comment.objects.select_related('post').order_by('-created_at')[:3]
		}


def version(request):
		return {'APP_VERSION': '3.23.2'}


def css_version(request):
		return {'css_version': settings.CSS_VERSION}