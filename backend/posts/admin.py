from django.contrib import admin

from .models import Post, Comment


class CommentsInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('id', 'text', 'author')
    readonly_fields = ('id', 'text', 'author')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'status', 'pub_date')
    list_display_links = ('title',)
    inlines = (CommentsInline,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author')
