from django.urls import path
from .views import (
    CategoryListCreateView,
    TransactionListCreateView,
    TransactionDetailView
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('<uuid:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
]
