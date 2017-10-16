from django.contrib import admin
from .models import Post


# class PostImageInline(admin.TabularInline):
#     model = PostImage
#     extra = 3


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    # inlines = [ PostImageInline, ]
admin.site.register(Post, PostAdmin)