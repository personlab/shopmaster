import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_shopmaster.settings')
import django
django.setup()

from django.db import connection

try:
		with connection.cursor() as cursor:
				cursor.execute("SELECT current_user, current_database()")
				print("DB User and Name:", cursor.fetchone())
				
				cursor.execute("SELECT 1")
				print("Test Query:", cursor.fetchone())
				
				from blog.models import Post
				print("Posts Count:", Post.objects.count())
except Exception as e:
		print("ERROR:", str(e))