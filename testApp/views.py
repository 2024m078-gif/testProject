from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from rest_framework import generics
import requests

from .models import Post
from .forms import PostForm
from .serializers import PostSerialize

# --- 1. お天気アプリ (Weather API) ---
def weather(request):
    locations = {
        'Kanazawa': {'lat': 36.59, 'lon': 136.60},
        'Tokyo': {'lat': 35.68, 'lon': 139.76},
        'Osaka': {'lat': 34.69, 'lon': 135.50},
        'Sapporo': {'lat': 43.06, 'lon': 141.35},
        'Naha': {'lat': 26.21, 'lon': 127.68},
    }

    city_name = 'Kanazawa'
    if request.GET.get('city') in locations:
        city_name = request.GET.get('city')

    lat = locations[city_name]['lat']
    lon = locations[city_name]['lon']

    api_url = (
        f'https://api.open-meteo.com/v1/forecast'
        f'?latitude={lat}&longitude={lon}&current_weather=true'
    )

    response = requests.get(api_url)
    data = response.json()

    context = {
        'city': city_name,
        'temperature': data['current_weather']['temperature'],
        'windspeed': data['current_weather']['windspeed'],
        'weathercode': data['current_weather']['weathercode'],
    }
    # templates/testApp/weather.html を使う場合は 'testApp/weather.html'
    return render(request, 'testApp/weather.html', context)

# --- 2. API Views (React/Frontend用) ---
class PostListAPIView(generics.ListAPIView): 
    queryset = Post.objects.all() 
    serializer_class = PostSerialize

# --- 3. タイムライン表示 (ListView) ---
class PostListView(ListView):
    model = Post
    template_name = "testApp/timeline.html" 
    context_object_name = 'posts'
    ordering = ['-created_at']

# --- 4. 投稿詳細 (DetailView) ---
class PostDetailView(DetailView):
    model = Post
    template_name = 'testApp/post_detail.html'
    context_object_name = 'post' # 個別投稿なので単数形が一般的

# --- 5. 新規投稿 (Function View) ---
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('timeline')
    else:
        form = PostForm()
    return render(request, 'testApp/post_new.html', {'form': form})

# --- 6. 投稿編集 (Function View) ---
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 投稿者以外が編集しようとしたら詳細ページへ戻す
    if request.user != post.author:
        return redirect('post_detail', pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'testApp/post_edit.html', {'form': form})

# --- 7. 投稿削除 (DeleteView) ---
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'testApp/post_confirm_delete.html'
    success_url = reverse_lazy('timeline')

    # 投稿者本人しか削除できないようにするチェック
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author