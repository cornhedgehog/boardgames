from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^categories/$', views.categories, name='categories'),
    url(r'^category/$', views.category, name='category'),
    url(r'^posts/$', views.posts, name='posts'),
    url(r'^post/$', views.post_create, name='post_create'),
    url(r'^post/(?P<post_slug>\w+)/$', views.post, name='post'),
    url(r'^post_teaser/(?P<post_id>\d+)/$', views.post_teaser, name='post_teaser'),
    url(r'^posts/(?P<category_slug>\w+)/$', views.posts_by_category, name='posts'),
    url(r'^posts_favourite/$', views.favposts, name='posts_favourite'),
    url(r'^post_published/(?P<post_slug>\w+)/$', views.post_published, name='post_published'),
    url(r'^post_unpublished/(?P<post_slug>\w+)/$', views.post_unpublished, name='post_unpublished'),
    url(r'^upload_pictures/(?P<post_slug>\w+)/$', views.upload_pictures, name='upload_picture'),
    url(r'^user_banned/(?P<user_id>\d+)/$', views.user_banned, name='user_banned'),
    url(r'^user_unbanned/(?P<user_id>\d+)/$', views.user_unbanned, name='user_unbanned'),
]
