from django.urls import path
from .views import PostList, PostDetail, PostCreate, NewsUpdate, NewsDelete, ArticlesUpdate, ArticlesDelete, PostSearch, upgrade_me
from .views import subscribe_to_category

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('articles/<int:pk>/', PostDetail.as_view(), name='article_detail'),
    path('news/search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('articles/create/', PostCreate.as_view(), name='article_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='articles_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('category/<int:pk>/subscribe/', subscribe_to_category, name='subscribe_to_category'),
]