from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from catalog.apps import CatalogConfig

from catalog.views import contacts, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    to_published, CategoryListView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('contacts/', contacts, name='contacts'),
    path('category/', CategoryListView.as_view(), name='category'),
    path('view/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='view'),
    path('create/', never_cache(ProductCreateView.as_view()), name='create_product'),
    path('update/<int:pk>/', never_cache(ProductUpdateView.as_view()), name='update_product'),
    path('to_published/<int:pk>/', to_published, name='to_published'),
]
