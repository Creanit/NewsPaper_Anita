from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Post

class PostList(ListView):
    model = Post
    ordering = ['-post_date']
    template_name = 'post_list.html'
    context_object_name = 'posts'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = "Новая статья каждую субботу!"
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'single_post.html'
    context_object_name = 'post'
