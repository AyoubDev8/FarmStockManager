from django.urls import path
from .views import (InventoryListView, AddInventoryView, EditInventoryView, InventoryDeleteView,
                    ProductListView, AddProductView, EditProductView, ProductDeleteView)

urlpatterns = [
    # Paths for raw material inventory
    path('list/', InventoryListView.as_view(), name='inventory_list'),
    path('add/', AddInventoryView.as_view(), name='add_inventory'),
    path('edit/<str:raw_material_code>/', EditInventoryView.as_view(), name='edit_inventory'),
    path('delete/<str:raw_material_code>/', InventoryDeleteView.as_view(), name='delete_inventory'),

    # Existing paths for products
    path('products/list/', ProductListView.as_view(), name='product_list'),
    path('products/add/', AddProductView.as_view(), name='add_product'),
    path('edit-product/<str:product_code>/', EditProductView.as_view(), name='editproduct'),
    path('delete-product/<pk>/', ProductDeleteView.as_view(), name='deleteproduct'),
]

