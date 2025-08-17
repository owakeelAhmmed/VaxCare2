from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Vaccine, VaccineSchedule, DoseBooking, CampaignReview, Campaign
from .serializers import VaccineSerializer, VaccinationScheduleSerializer, DoseBookingSerializer,CampaignReviewSerializer, CampaignSerializer, CampaignBookingSerializer, CampaignBooking
from auth_app.permissions import IsDoctor
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsPatient

# Create your views here.


class VaccineViewSet(viewsets.ModelViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer
    permission_classes = [IsDoctor]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class VaccinationScheduleViewSet(viewsets.ModelViewSet):
    queryset = VaccineSchedule.objects.all()
    serializer_class = VaccinationScheduleSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class DoseBookingViewSet(viewsets.ModelViewSet):
    serializer_class = DoseBookingSerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return DoseBooking.objects.filter(patient=self.request.user)
        return DoseBooking.objects.none()

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CampaignBookingListCreateView(viewsets.ModelViewSet):
    queryset = CampaignBooking.objects.all()
    serializer_class = CampaignBookingSerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

class CampaignBookingDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = CampaignBookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CampaignBooking.objects.filter(patient=self.request.user)




class CampaignReviewViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignReviewSerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CampaignReview.objects.none()
        return CampaignReview.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)