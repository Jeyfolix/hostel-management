from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HostelViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'hostels', HostelViewSet, basename='hostel')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('hostels/featured/', HostelViewSet.as_view({'get': 'featured'}), name='hostels-featured'),
    path('hostels/locations/', HostelViewSet.as_view({'get': 'locations'}), name='hostels-locations'),
]
