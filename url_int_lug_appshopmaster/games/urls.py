from django.urls import path
from django.views.decorators.cache import cache_page

from games.views import GamesView

app_name = 'games'


urlpatterns = [
		path('', GamesView.as_view(), name='games'),
]