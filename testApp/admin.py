from django.contrib import admin
from .models import Post
# 「Postモデルを、この管理サイトで扱えるように登録します」という命令
admin.site.register(Post)
# Register your models here.
