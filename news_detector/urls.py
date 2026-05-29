"""
URL configuration for news_detector project.

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
from django.urls import path, include
from analyzer.views import index
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    # path("", index, name="index"),  # 设置主页 url 为""
    path("analyzer/", include("analyzer.urls")),  # 对项目 analyzer 分发一个路由
    path('accounts/', include('accounts.urls')),


]

# 仅在开发环境（DEBUG=True）启用静态文件服务

# urls.py 底部添加
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
