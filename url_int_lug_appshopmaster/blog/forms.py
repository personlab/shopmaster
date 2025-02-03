from django import forms
from .models import Comment, CommentRecentPost


class CommentForm(forms.ModelForm):
		class Meta:
				model = Comment
				fields = ['text']

		def __init__(self, *args, **kwargs):
				self.user = kwargs.pop('user', None)  # Извлекаем пользователя
				super().__init__(*args, **kwargs)

		def save(self, commit=True):
				comment = super().save(commit=False)
				if self.user and self.user.is_authenticated:
						comment.author = self.user.username
				else:
						comment.author = 'Anonymous'
				if commit:
						comment.save()
				return comment


class CommentRecentForm(forms.ModelForm):
		class Meta:
				model = CommentRecentPost
				fields = ['text']

		def __init__(self, *args, **kwargs):
				self.user = kwargs.pop('user', None)  # Извлекаем пользователя
				super().__init__(*args, **kwargs)

		def save(self, commit=True):
				comment = super().save(commit=False)
				if self.user and self.user.is_authenticated:
						comment.author = self.user.username
				else:
						comment.author = 'Anonymous'
				if commit:
						comment.save()
				return comment