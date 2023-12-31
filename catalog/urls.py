from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('contacts/', contacts, name='contacts'),
    path('view/<int:pk>/', ProductDetailView.as_view(), name='view'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
]
