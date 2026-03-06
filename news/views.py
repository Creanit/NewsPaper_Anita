from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    ordering = ['-post_date']
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context_time = super().get_context_data(**kwargs)
        context_time['time_now'] = datetime.utcnow()
        context_time['next_post'] = "Новая статья каждую субботу!"
        return context_time

class PostDetail(DetailView):
    model = Post
    template_name = 'single_post.html'
    context_object_name = 'post'

class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 5
    filterset_class = PostFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        if not self.request.GET:
            return Post.objects.none()
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        form.instance.post_type = 'NL'
        return super().form_valid(form)

class ArticlesCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        form.instance.post_type = 'BP'
        return super().form_valid(form)

class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    queryset = Post.objects.filter(post_type='NL')
    template_name = 'post_edit.html'

    def form_valid(self, form):
        form.instance.post_type = 'NL'
        return super().form_valid(form)

class ArticlesUpdate(UpdateView):
    form_class = PostForm
    model = Post
    queryset = Post.objects.filter(post_type='BP')
    template_name = 'post_edit.html'

    def form_valid(self, form):
        form.instance.post_type = 'BP'
        return super().form_valid(form)

class NewsDelete(DeleteView):
    model = Post
    queryset = Post.objects.filter(post_type='NL')
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class ArticlesDelete(DeleteView):
    model = Post
    queryset = Post.objects.filter(post_type='BP')
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')