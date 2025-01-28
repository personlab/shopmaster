from django.urls import path

from users.views import LoginViews, ProfileView, LogoutView, RegistrationView

app_name = 'users'


urlpatterns = [
		path('login/', LoginViews.as_view(), name='login'),
		path('registration/', RegistrationView.as_view(), name='registration'),
		path('profile/', ProfileView.as_view(), name='profile'),
		path('logout/', LogoutView.as_view(), name='logout'),
]