from django.contrib import auth
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from urllib import request
from django.conf import settings
from django.http import Http404, HttpResponseRedirect, JsonResponse
import requests
from django.db.models import F, CharField, Value
from itertools import chain

from users.forms import UserLoginForm, UserRegistrationForm


class LoginViews(View):

		def get(self, request):
				form = UserLoginForm()
				context = {
						'title': 'TonGameApp - Авторизация|Регистрация',
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
								return HttpResponseRedirect(reverse('blog:post_list'))
				context = {
						'title': 'TonGameApp - Авторизация|Регистрация',
						'form': form
				}
				return render(request, 'users/login.html', context=context)
		

		
class RegistrationView(View):
			
		def get(self, request):
				form = UserRegistrationForm()
				context = {
						'title': 'TonGameApp - Авторизация|Регистрация',
						'form': form
				}
				return render(request, 'users/registration.html', context=context)

		def post(self, request):
				form = UserRegistrationForm(data=request.POST)
				if form.is_valid():
						form.save()
						user = form.instance
						auth.login(request, user)
						return HttpResponseRedirect(reverse('main:index'))
				
				context = {
						'title': 'TonGameApp - Авторизация|Регистрация',
						'form': form
				}
				return render(request, 'users/registration.html', context=context)
			


class ProfileView(View):
		
		def get(self, request):
				context = {
					'title': 'TonGameApp - Профиль',
				}

				return render(request, 'users/profile.html', context=context)
		

class LogoutView(View):
		
		def get(self, request):
				auth.logout(request)
				return redirect(reverse('main:index'))