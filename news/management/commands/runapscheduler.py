import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Category, Post


logger = logging.getLogger(__name__)


def send_weekly_newsletter():
    week_ago = timezone.now() - timezone.timedelta(days=7)

    categories = Category.objects.all()

    for category in categories:
        posts = Post.objects.filter(
            post_categories=category,
            post_date__gte=week_ago,
            post_type='NL',
        ).distinct()

        if not posts.exists():
            continue

        subscribers = category.subscribers.all()

        for user in subscribers:
            if user.email:
                html_content = render_to_string(
                    'weekly_newsletter.html',
                    {
                        'user': user,
                        'category': category,
                        'posts': posts,
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=f'Новости за неделю в категории {category.category_name}',
                    body=f'Здравствуй, {user.username}! Новые статьи за неделю в твоём любимом разделе.',
                    from_email=None,
                    to=[user.email],
                )

                msg.attach_alternative(html_content, "text/html")
                msg.send()


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_newsletter,
            trigger=CronTrigger(day_of_week="fri", hour="08", minute="00"),
            id="send_weekly_newsletter",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: send_weekly_newsletter")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: delete_old_job_executions")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")