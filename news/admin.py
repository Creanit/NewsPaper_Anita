from django.contrib import admin
from .models import Category, Author, Post, PostCategory, Comment

class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "post_type", "post_date", "author")
    list_filter = ("post_type", "post_date", "author")
    search_fields = ("title", "content")
    inlines = [PostCategoryInline]


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Comment)

admin.site.register(PostCategory)