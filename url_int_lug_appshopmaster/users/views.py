from email import message
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib import auth, messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from urllib import request
from django.conf import settings
from django.http import Http404, HttpResponseRedirect, JsonResponse
import requests
from django.db.models import F, CharField, Value
from itertools import chain

from traitlets import Instance

from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm


class LoginViews(View):

		def get(self, request):
				form = UserLoginForm()
				context = {
						'title': 'GameTonApp - Авторизация',
						'description': 'Авторизация в приложении GameTonApp',
						'form': form
				}
				return render(request, 'users/login.html', context=context)

		def post(self, request):
				form = UserLoginForm(data=request.POST)
				if form.is_valid():
						username = request.POST['username']
						password = request.POST['password']
						user = auth.authenticate(username=username, password=password)
						if user:
								auth.login(request, user)
								messages.success(request, f"{username}, Вы вошли в аккаунт")
								return HttpResponseRedirect(reverse('blog:post_list'))
				context = {
						'title': 'TonGameApp - Авторизация',
						'description': 'Авторизация в приложении GameTonApp',
						'form': form
				}
				return render(request, 'users/login.html', context=context)
		

		
class RegistrationView(View):
			
		def get(self, request):
				form = UserRegistrationForm()
				context = {
						'title': 'GameTonApp - Регистрация',
						'description': 'Регистрация в приложении GameTonApp',
						'form': form
				}
				return render(request, 'users/registration.html', context=context)

		def post(self, request):
				form = UserRegistrationForm(data=request.POST)
				if form.is_valid():
						form.save()
						user = form.instance
						auth.login(request, user)
						messages.success(request, f"{user.username}, Вы успешно зарегистрироались")
						return HttpResponseRedirect(reverse('main:index'))
				
				context = {
						'title': 'GameTonApp - Регистрация',
						'description': 'Регистрация в приложении GameTonApp',
						'form': form
				}
				return render(request, 'users/registration.html', context=context)
			

def login_required_404(view_func):
	
	@login_required
	def _wrapped_view(request, *args, **kwargs):
			if request.user.is_authenticated:
					return view_func(request, *args, **kwargs)
			else:
					raise Http404("Страница не найдена")
	return _wrapped_view


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
		
		def get(self, request):
				form = ProfileForm(instance=request.user)
				context = {
					'title': 'GameTonApp - Профиль',
					'form': form
				}

				return render(request, 'users/profile.html', context=context)
		
		def post(self, request):
				form = ProfileForm(data=request.POST, files=request.FILES, instance=request.user)
				if form.is_valid():
						form.save()
						messages.success(request, "Профиль успешно обновлен")
						return HttpResponseRedirect(reverse('user:profile'))
				
				context = {
					'title': 'GameTonApp - Профиль',
					'form': form
				}

				# Добавьте здесь вывод ошибок, если они есть
				if form.errors:
						print(form.errors)

				return render(request, 'users/profile.html', context=context)

@method_decorator(login_required, name='dispatch')
class LogoutView(View):
		
		def get(self, request):
				# messages.success(request, f"{request.user.username}, До встерчи!")
				auth.logout(request)
				return redirect(reverse('main:index'))