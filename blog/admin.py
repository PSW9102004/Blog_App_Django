from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'date_posted')
    list_filter = ('status', 'date_posted')
    search_fields = ('title', 'subtitle', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}

# The TagAdmin class is removed because django-taggit handles tags internally.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'date_posted')
    search_fields = ('content', 'author__username', 'post__title')
