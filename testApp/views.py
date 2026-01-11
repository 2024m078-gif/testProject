from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.views.generic import ListView, DetailView, DeleteView   # ← DeleteViewを追加
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy  
from .serializers import PostSerialize
from rest_framework import generics 
import requests

def weather(request):
    # 1. 都市と座標の辞書
    locations = {
        'Kanazawa': {'lat': 36.59, 'lon': 136.60},
        'Tokyo': {'lat': 35.68, 'lon': 139.76},
        'Osaka': {'lat': 34.69, 'lon': 135.50},
        'Sapporo': {'lat': 43.06, 'lon': 141.35},
        'Naha': {'lat': 26.21, 'lon': 127.68},
    }

    # 2. デフォルトは金沢（GETで指定があれば変更）
    city_name = 'Kanazawa'
    if request.GET.get('city') in locations:
        city_name = request.GET.get('city')

    # 3. 緯度・経度を取得
    lat = locations[city_name]['lat']
    lon = locations[city_name]['lon']

    # 4. API URL（※ true の改行ミスを修正）
    api_url = (
        f'https://api.open-meteo.com/v1/forecast'
        f'?latitude={lat}&longitude={lon}&current_weather=true'
    )

    # 5. APIからデータ取得
    response = requests.get(api_url)
    data = response.json()

    # 6. テンプレートに渡すデータ
    context = {
        'city': city_name,
        'temperature': data['current_weather']['temperature'],
        'windspeed': data['current_weather']['windspeed'],
        'weathercode': data['current_weather']['weathercode'],
    }

    return render(request, 'weather.html', context)



class PostListAPIView(generics.ListAPIView): 
    queryset = Post.objects.all() 
    serializer_class = PostSerialize




class PostListView(ListView):
    model = Post
    template_name = "testApp/timeline.html" 
    context_object_name = 'posts'
    ordering = ['-created_at']


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'posts'

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 投稿者以外が編集しようとしたら弾く
    if request.user != post.author:
        return redirect('post_detail', pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'post_edit.html', {'form': form})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('timeline')

    # 投稿者以外は削除不可
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('timeline')  # 適宜変更
    else:
        form = PostForm()
    return render(request, 'post_new.html', {'form': form})