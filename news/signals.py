from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post


@receiver(m2m_changed, sender=Post.post_categories.through)
def notify_subscribers(sender, instance, action, pk_set, **kwargs):
    if action != 'post_add':
        return

    if instance.post_type != 'NL':
        return

    subscribers = []

    for category in instance.post_categories.filter(pk__in=pk_set):
        subscribers += list(category.subscribers.all())

    subscribers = list(set(subscribers))

    for user in subscribers:
        if user.email:
            html_content = render_to_string(
                'post_created_email.html',
                {
                    'post': instance,
                    'user': user,
                }
            )

            msg = EmailMultiAlternatives(
                subject=instance.title,
                body=f'Здравствуй, {user.username}. Новая статья в твоём любимом разделе!',
                from_email=None,
                to=[user.email],
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()