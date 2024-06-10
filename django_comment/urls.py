"""django_comment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from . import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('comments/', include('comments.urls')),
    # path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),  # ルートURLで静的なindex.htmlを表示
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path("", include(debug_toolbar.urls)))


# 開発環境での静的ファイルの配信設定
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))
