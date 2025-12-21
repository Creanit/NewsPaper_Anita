from django.db import models
from django.conf import settings
from django.apps import apps


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name

class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        Post = apps.get_model('news', 'Post')
        Comment = apps.get_model('news', 'Comment')

        posts_sum = (
                Post.objects
                .filter(author=self)
                .aggregate(total=models.Sum('post_rating'))
                .get('total') or 0
        )

        author_comments_sum = (
                Comment.objects
                .filter(user=self.user)
                .aggregate(total=models.Sum('comment_rating'))
                .get('total') or 0
        )

        post_comments_sum = (
                Comment.objects
                .filter(post__author=self)
                .aggregate(total=models.Sum('comment_rating'))
                .get('total') or 0
        )

        self.author_rating = posts_sum * 3 + author_comments_sum + post_comments_sum
        self.save()

class Post(models.Model):
    newsletter = 'NL'
    blogpost = 'BP'

    POST_TYPE_CHOICES = [
        (newsletter, 'Новости'),
        (blogpost, 'Статья'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPE_CHOICES, default=newsletter)
    post_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    post_rating = models.IntegerField(default=0)
    post_categories = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return self.title

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        if len(self.content) <= 124:
            return self.content
        else:
            return self.content[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField()
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


