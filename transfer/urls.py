from django.urls import path
from .views import (
    TransferListView,
    AddTransferView,
    EditTransferView,
    DeleteTransferView,
)

urlpatterns = [
    path('list/', TransferListView.as_view(), name='transfer_list'),
    path('add/', AddTransferView.as_view(), name='add_transfer'),
    path('edit/<int:transfer_id>/', EditTransferView.as_view(), name='edit_transfer'),
    path('delete/<int:transfer_id>/', DeleteTransferView.as_view(), name='delete_transfer'),
]
