from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from users.views import LoginViews, ProfileView, LogoutView, RegistrationView

app_name = 'users'


urlpatterns = [
		path('login/', LoginViews.as_view(), name='login'),
		path('registration/', RegistrationView.as_view(), name='registration'),
		path('profile/', ProfileView.as_view(), name='profile'),
		path('logout/', LogoutView.as_view(), name='logout'),

		# -- начало блока сброса пароля ввод пароля--
		path('password_reset_form/', auth_views.PasswordResetView.as_view(
				template_name='users/password_reset_form.html',
				email_template_name='users/password_reset_email.html',
				success_url=reverse_lazy('users:password_reset_done'),
				extra_email_context={'protocol': 'https', 'domain': 'gameton.app'}
		), name='password_reset_form'),
		path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
			template_name='users/password_reset_done.html'), name='password_reset_done'),
		path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
			template_name='users/password_reset_confirm.html',
			success_url=reverse_lazy('users:password_reset_complete')
		), name='password_reset_confirm'),
		path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(
			template_name='users/password_reset_complete.html'), name='password_reset_complete'),
		# -- конец блока восстановления пароля --
]