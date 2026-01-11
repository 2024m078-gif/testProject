from rest_framework import serializers
from .models import Post

class PostSerialize(serializers.ModelSerializer):
    class Meta:
        model = Post 
        fields = ['id', 'content', 'created_at']