from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Post, Category


@shared_task
def send_new_post_notifications(post_id):
    post = Post.objects.get(pk=post_id)
    categories = post.post_categories.all()

    subscribers = set()

    for category in categories:
        subscribers.update(category.subscribers.all())

    for user in subscribers:
        if user.email:
            html_content = render_to_string(
                'news/new_post_email.html',
                {
                    'post': post,
                    'user': user,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'Новая публикация: {post.title}',
                body=post.preview(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()


@shared_task
def send_weekly_news():
    week_ago = timezone.now() - timedelta(days=7)

    posts = Post.objects.filter(
        post_date__gte=week_ago,
        post_type=Post.newsletter,
    )

    categories = Category.objects.all()

    for category in categories:
        category_posts = posts.filter(post_categories=category)
        subscribers = category.subscribers.all()

        if not category_posts.exists():
            continue

        for user in subscribers:
            if user.email:
                html_content = render_to_string(
                    'news/weekly_news_email.html',
                    {
                        'posts': category_posts,
                        'category': category,
                        'user': user,
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=f'Новости за неделю: {category.category_name}',
                    body='Свежие новости за неделю',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email],
                )
                msg.attach_alternative(html_content, 'text/html')
                msg.send()