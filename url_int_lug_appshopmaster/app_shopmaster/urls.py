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
from django.contrib import admin
from django.urls import include, path

# from django.conf import settings # - переключаем на эти настройки, если в нашем файле настроек чего-то нет и он не работает должным образом.
from app_shopmaster import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

from blog import urls


urlpatterns = [
		path('admin/', admin.site.urls),
		path('', include('main.urls', namespace='main')),
		path('catalog/', include('goods.urls', namespace='catalog')),
		path('blog/', include('blog.urls', namespace='blog'))
]

if settings.DEBUG:
	urlpatterns += [
			path("__debug__/", include("debug_toolbar.urls")),
		]
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""
www.shopmaster.info/admin/
www.shopmaster.info/
www.shopmaster.info/about/
www.shopmaster.info/catalog/
www.shopmaster.info/catalog/product

"""