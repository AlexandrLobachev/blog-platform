from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model

from posts.models import Post


User = get_user_model()


class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    fields = ('id', 'title', 'text', 'status', 'pub_date')


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    inlines = (PostInline,)
