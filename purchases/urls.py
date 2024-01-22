from django.urls import path
from . import views

urlpatterns = [
    # Existing supplier URLs
    path('suppliers/', views.SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/add/', views.AddSupplierView.as_view(), name='add_supplier'),
    path('suppliers/edit/<str:code>/', views.EditSupplierView.as_view(), name='edit_supplier'),
    path('suppliers/delete/<str:code>/', views.SupplierDeleteView.as_view(), name='delete_supplier'),

    # URLs for Purchase
    path('', views.PurchaseListView.as_view(), name='purchase_list'),
    path('add/', views.AddPurchaseView.as_view(), name='add_purchase'),
    path('edit/<str:purchase_code>/', views.EditPurchaseView.as_view(), name='edit_purchase'),
    path('delete/<str:purchase_code>/', views.PurchaseDeleteView.as_view(), name='delete_purchase'),
]
