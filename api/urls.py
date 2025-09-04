from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListCreate.as_view(), name='product_list_create'),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDestroy.as_view(), name='product_rud'),
]
