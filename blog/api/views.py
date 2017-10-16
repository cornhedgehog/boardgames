import io, os
import random

from django.contrib.auth.models import User
from django.core.files import File
from PIL import Image
from django.utils.text import slugify
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.utils import json
from blog.api.serializers import CategorySerializer, PostSerializer, PostTeaserSerializer, FavPostSerializer
from blog.models import Category, Post, FavPosts, PostImage


##############
# Категории
##############
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def categories(request):
    """
    Получить все категории  
    """
    if request.method == 'GET':
        countries = Category.objects.all()
        serialized = CategorySerializer(list(countries), many=True) # serializers.serialize('json', countries)
        return Response(serialized.data)

@api_view(['POST'])
@permission_classes((IsAdminUser, ))
def category(request):
    """
    Добавить новую категорию
    """
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        new_category = Category.objects.create(name=body['name'], slug=body['slug'])
        new_category.save()
        return Response(status = status.HTTP_201_CREATED)


##############
# Посты
##############
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def posts(request):
    """
    Получить все посты
    """
    if request.method == 'GET':
        posts = Post.objects.all()
        serialized = PostSerializer(list(posts), many=True)
        return Response(serialized.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def posts_by_category(request, category_slug):
    """
    Получить все посты категории
    """
    if request.method == 'GET':
        posts = Post.objects.filter(category__slug__exact=category_slug)
        serialized = PostSerializer(list(posts), many=True)
        return Response(serialized.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def post(request, post_slug):
    """
    Получить пост по ссылке, обновить пост, удалить пост
    """
    if request.method == 'GET':
        post = Post.objects.get(slug=post_slug)
        serialized = PostSerializer(post)
        return Response(serialized.data)

    elif request.method == 'PUT':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        post = Post.objects.get(slug=post_slug)
        post.title = body['title']
        post.subtitle=body['subtitle']
        post.category_id=body['category_id']
        post.body=body['body']
        post.body_preview=body['body'][:70]
        post.save()
        return Response(status=status.HTTP_202_ACCEPTED)

    elif request.method == 'DELETE':
        post = Post.objects.get(slug=post_slug)
        post.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def post_create(request):
    """
    Создать пост
    """
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        Post.objects.create(title=body['title'],
                                   subtitle=body['subtitle'],
                                   category_id = body['category_id'],
                                   body=body['body'],
                                   author_id=request.user.id,
                                   slug= slugify(str(random.randint(10000, 100000)) + ' ' + body['title']),
                                   status='draft',
                                   body_preview=body['body'][:70])

        return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def upload_pictures(request, post_slug):
    """
    Загрузить изображения
    """
    if request.method == 'POST':
        filelist = os.listdir('tmp')
        for eachfile in filelist:
            try:
                os.remove(os.path.join('tmp/', eachfile))
            except OSError as e:
                pass
        image_names = request.data['image_names']
        for image_name in image_names:
            for f in request.FILES.getlist(image_name):
                if (f.content_type == 'image/jpeg') or (f.content_type == 'image/png'):
                    image_pil = Image.open(f.file)
                    max_size = 4 * 1024 * 768
                    if f._size > max_size:
                        image_pil = image_pil.resize((1024, 768), Image.ANTIALIAS)
                    imgByteArr = io.BytesIO()
                    if f.content_type == 'image/jpeg':
                        image_pil.save(imgByteArr, format='JPEG')
                        imgByteArr = imgByteArr.getvalue()
                        with open('tmp/tmp.jpeg', 'wb') as file:
                            file.write(imgByteArr)
                        reopen = open('tmp/tmp.jpeg', 'rb')
                    elif f.content_type == 'image/png':
                        image_pil.save(imgByteArr, format='PNG')
                        imgByteArr = imgByteArr.getvalue()
                        with open('tmp/tmp.png', 'wb') as file:
                            file.write(imgByteArr)
                        reopen = open('tmp/tmp.png', 'rb')
                    img_in_memory = File(reopen)
                    img = PostImage.objects.create()
                    img.title = f.name
                    img.post_slug = post_slug
                    img.image = img_in_memory
                    img.save()
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def post_teaser(request, post_id):
    """
    Загрузить тизер поста по id
    """
    if request.method == 'GET':
        post = Post.objects.get(pk=post_id)
        serialized = PostTeaserSerializer(post)
        return Response(serialized.data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def favposts(request):
    """
    Получить все избранные посты, добавить пост в избранное, удалить пост из избранного
    """
    if request.method == 'GET':
        favposts = FavPosts.objects.filter(user=request.user.id)
        favpost_ids_serialized = FavPostSerializer(list(favposts), many=True)
        post_ids = list()
        for post in favpost_ids_serialized.data:
            post_ids.append(post['post'])
        posts_starred_as_feed = Post.objects.filter(pk__in=post_ids)
        serialized = PostSerializer(list(posts_starred_as_feed), many=True)
        return Response(serialized.data)
    else:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        post_id = body['post_id']
        post_starred = FavPosts.objects.filter(post=post_id, user=request.user.id)
        if request.method == 'POST':
            if post_starred.count() == 0:
                add_post = FavPosts.objects.create(post_id=post_id, user_id=request.user.id)
                add_post.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_409_CONFLICT)
        if request.method == 'DELETE':
            post_starred.delete()
            return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes((IsAdminUser, ))
def post_published(request, post_slug):
    """
    Сделать пост опубликованным
    """
    if request.method == 'PUT':
        post = Post.objects.get(slug=post_slug)
        post.status = 'published'
        post.save()
        return Response(status = status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes((IsAdminUser, ))
def post_unpublished(request, post_slug):
    """
    Сделать пост неопубликованным
    """
    if request.method == 'PUT':
        post = Post.objects.get(slug=post_slug)
        post.status = 'draft'
        post.save()
        return Response(status=status.HTTP_200_OK)

#############
# Пользователи
##########
@api_view(['PUT'])
@permission_classes((IsAdminUser, ))
def user_banned(request, user_id):
    """
    Забанить пользователя
    """
    if request.method == 'PUT':
        user = User.objects.get(pk=user_id)
        user.is_active = 0
        user.save()
        return Response(status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes((IsAdminUser, ))
def user_unbanned(request, user_id):
    """
    Забанить пользователя
    """
    if request.method == 'PUT':
        user = User.objects.get(pk=user_id)
        user.is_active = 1
        user.save()
        return Response(status=status.HTTP_200_OK)