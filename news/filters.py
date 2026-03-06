import django_filters
from django import forms
from .models import Post

class PostFilter(django_filters.FilterSet):
    post_date = django_filters.DateFilter(
        field_name='post_date',
        lookup_expr='gt',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label= 'Published after:'
    )

    class Meta:
       model = Post
       fields = {
           'title': ['icontains'],
           'author': ['exact'],
       }