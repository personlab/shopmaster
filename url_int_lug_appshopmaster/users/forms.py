from dataclasses import field, fields
from pyexpat import model
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class UserLoginForm(AuthenticationForm):
		
		username = forms.CharField()
		password = forms.CharField()
		
		# username = forms.CharField(
		# 		widget=forms.TextInput(attrs={"autofocus": True,
		# 															'class': 'input__fields',
		# 															'placeholder': 'Ваше имя'})
		# )
		# password = forms.CharField(
		# 		widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
		# 																 'class': 'input__fields',
		# 																 'id': 'password',
		# 																 'placeholder': 'Пароль'})
		# )

		
		class Meta:
				model = User
				field = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
		
		# first_name = forms.CharField(
		# 			widget=forms.TextInput(
		# 				attrs={
		# 					"class": "input__fields",
		# 					"placeholder": "Ваше имя",
		# 				}
		# 		)
		# )

		# last_name = forms.CharField(
		# 		widget=forms.TextInput(
		# 				attrs={
		# 						"class": "input__fields",
		# 						"placeholder": "Ваша фамилия",
		# 				}
		# 		)
		# )
		# username = forms.CharField(
		# 		widget=forms.TextInput(
		# 				attrs={
		# 						"class": "input__fields",
		# 						"placeholder": "Ваш никнейм",
		# 				}
		# 		)
		# )
		# email = forms.CharField(
		# 		widget=forms.EmailInput(
		# 				attrs={
		# 						"class": "input__fields",
		# 						"placeholder": "Ваш email",
		# 				}
		# 		)
		# )
		# password1 = forms.CharField(
		# 		widget=forms.PasswordInput(
		# 				attrs={
		# 						"class": "input__fields",
		# 						"placeholder": "Введите пароль",
		# 				}
		# 		)
		# )
		# password2 = forms.CharField(
		# 		widget=forms.PasswordInput(
		# 				attrs={
		# 						"class": "input__fields",
		# 						"placeholder": "Повторите пароль",
		# 				}
		# 		)
		# )

		first_name = forms.CharField()
		last_name = forms.CharField()
		username = forms.CharField()
		email = forms.CharField()
		password1 = forms.CharField()
		password2 = forms.CharField()


		class Meta:
				model = User
				fields = (
					"first_name",
					"last_name",
					"username",
					"email",
					"password1",
					"password2",
				)