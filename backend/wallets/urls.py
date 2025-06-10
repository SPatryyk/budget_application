from django.urls import path
from .views import (
    WalletListCreateView, WalletDetailView,
    TransferListCreateView, TransferDetailView
)

urlpatterns = [
    path('', WalletListCreateView.as_view(), name='wallet-list-create'),
    path('<uuid:pk>/', WalletDetailView.as_view(), name='wallet-detail'),

    path('transfers/', TransferListCreateView.as_view(),
         name='transfer-list-create'),
    path('transfers/<uuid:pk>/', TransferDetailView.as_view(),
         name='transfer-detail'),
]
