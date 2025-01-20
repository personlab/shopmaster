from django.urls import path

from users.views import LoginViews, RegistrationView, ProfileView, LogoutView

app_name = 'users'


urlpatterns = [
		path('login/', LoginViews.as_view(), name='log_reg'),
		path('registration/', RegistrationView.as_view(), name='registration'),
		path('profile/', ProfileView.as_view(), name='profile'),
		path('logout/', LogoutView.as_view(), name='logout'),
]