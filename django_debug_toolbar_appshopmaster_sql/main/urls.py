"""
URL configuration for appshopmaster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from main.views import IndexView, AboutView, ContactView, DroppView
app_name = 'main'


urlpatterns = [
		path('', IndexView.as_view(), name='index'),
		path('about/', AboutView.as_view(), name='about'),
		path('contact/', ContactView.as_view(), name='contact'),
		path('drop-shipping/', DroppView.as_view(), name='drop-shipping')
]