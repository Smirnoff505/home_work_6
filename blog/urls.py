from django.urls import path
from django.views.decorators.cache import never_cache

from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView, toggle_activity

app_name = BlogConfig.name

urlpatterns = [
    path('create/', never_cache(BlogCreateView.as_view()), name='create'),
    path('list/', BlogListView.as_view(), name='list'),
    path('detail/<str:slug>/', BlogDetailView.as_view(), name='detail'),
    path('edit/<int:pk>/', never_cache(BlogUpdateView.as_view()), name='edit'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
]
