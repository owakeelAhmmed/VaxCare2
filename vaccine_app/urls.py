from rest_framework.routers import DefaultRouter
from .views import VaccineViewSet, VaccinationScheduleViewSet, DoseBookingViewSet, CampaignReviewViewSet, CampaignViewSet, CampaignBookingListCreateView, CampaignBookingDetailView


router = DefaultRouter()
router.register('vaccines', VaccineViewSet, basename='vaccine')
router.register('campaigns', CampaignViewSet, basename='campaign')
router.register('schedules', VaccinationScheduleViewSet, basename='schedule')



router.register('dose-bookings', DoseBookingViewSet, basename='dose-booking')
router.register('campaigns-booking', CampaignBookingListCreateView, basename='campaign-booking')
router.register('campaign-reviews', CampaignReviewViewSet, basename='campaign-review')

urlpatterns = router.urls
