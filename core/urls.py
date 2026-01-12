"""
URL configuration for Django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

# testApp/urls.py （またはプロジェクトurlsでincludeしている箇所）
# core/urls.py
from django.contrib import admin
from django.urls import path,include
from testApp.views import PostListView, PostDetailView, PostDeleteView,PostListAPIView
from testApp import views
from django.conf import settings #

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', PostListView.as_view(), name='timeline'),  # ← as_view() 必須
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),  # ← as_view() 必須
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),  # ← as_view() 必須
    path('post/new/', views.post_new, name='post_new'),  # 関数ビューはそのまま
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),  # 関数ビュー
    path("api/posts/",PostListAPIView.as_view()),
    path('api/weather/', views.weather, name='weather'),
]