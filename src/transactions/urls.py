from django.urls import path
from .views import (
    home_view,
    SaleListView,
    SaleDetailView,
)

app_name = 'transactions'

urlpatterns = [
    path('', home_view, name='home'),
    path('transactions/', SaleListView.as_view(), name='list'),
    path('transactions/<pk>/', SaleDetailView.as_view(), name='detail'),

]