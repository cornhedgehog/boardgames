from rest_framework import serializers
from blog.models import Category, Post, FavPosts


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'subtitle', 'body_preview', 'body')


class FavPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavPosts
        fields = ('id', 'post', 'user')


class PostTeaserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'subtitle', 'slug', 'body_preview')
