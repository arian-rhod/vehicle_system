from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = router.urls