from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ColorViewSet, SizeViewSet, DeliveryLocationViewSet, DashboardStatsView

router = DefaultRouter()
router.register(r'colors', ColorViewSet)
router.register(r'sizes', SizeViewSet)
router.register(r'delivery-locations', DeliveryLocationViewSet)

urlpatterns = [
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('', include(router.urls)),
]
