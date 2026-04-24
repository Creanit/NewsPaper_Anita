from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post
from .filters import PostFilter
from .forms import PostForm

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class PostList(ListView):
    model = Post
    ordering = ['-post_date']
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = "Новая статья каждую субботу!"

        if self.request.user.is_authenticated:
            context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()

        return context

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

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)

        if self.request.path == '/news/create/':
            post.post_type = 'NL'
        elif self.request.path == '/articles/create/':
            post.post_type = 'BP'

        post.save()
        self.object = post
        return super().form_valid(form)

class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    queryset = Post.objects.filter(post_type='NL')
    template_name = 'post_edit.html'

    def form_valid(self, form):
        form.instance.post_type = 'NL'
        return super().form_valid(form)

class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
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

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')