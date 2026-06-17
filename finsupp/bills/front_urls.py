from django.urls import path
from .views_front import BillListView, BillDetailView

app_name = 'bills'

urlpatterns = [
    path('', BillListView.as_view(), name='list'),
    path('<int:pk>/', BillDetailView.as_view(), name='detail'),
]
