from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BillViewSet
from . import views_front

router = DefaultRouter()
router.register(r'bills', BillViewSet, basename='bill')

urlpatterns = router.urls
