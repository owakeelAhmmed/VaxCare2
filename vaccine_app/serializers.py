from rest_framework import serializers
from .models import Vaccine, VaccineSchedule, DoseBooking
from django.utils import timezone
from datetime import timedelta
from .models import CampaignReview, Campaign, CampaignBooking
from django.contrib.auth import get_user_model



User = get_user_model()

class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = '__all__'
        read_only_fields = ('created_by',)


class VaccinationScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineSchedule
        fields = ['campaign', 'vaccine', 'date', 'time', 'location', 'created_by']

# class DoseBookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DoseBooking
#         fields = ['id', 'schedule', 'first_dose_date', 'second_dose_date']
#         read_only_fields = ('second_dose_date',)

#     def create(self, validated_data):
#         user = self.context['request'].user
#         if user.role.lower() != 'patient':
#             raise serializers.ValidationError("Only patients can book doses.")
#         validated_data['patient'] = user
#         first_date = validated_data['first_dose_date']
#         validated_data['second_dose_date'] = first_date + timedelta(days=28)
#         return super().create(validated_data)

class DoseBookingSerializer(serializers.ModelSerializer):
    first_dose_date = serializers.DateField(source='schedule.date', read_only=True)

    class Meta:
        model = DoseBooking
        fields = ['id', 'schedule', 'first_dose_date', 'second_dose_date']
        read_only_fields = ['id''first_dose_date', 'second_dose_date']

    def validate_schedule(self, value):
        if value.date < timezone.now().date():
            raise serializers.ValidationError("Cannot book a schedule in the past.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['patient'] = user

        first_date = validated_data['schedule'].date
        validated_data['second_dose_date'] = first_date + timedelta(days=28)

        return super().create(validated_data)


# class CampaignSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Campaign
#         fields = '__all__'
#         read_only_fields = ('created_by',)


class CampaignSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = Campaign
        fields = [
            'id',
            'name',
            'vaccine_type',
            'start_date',
            'end_date',
            'dose_interval_days',
            'created_by',
            'created_by_name',
        ]
        read_only_fields = ['id', 'created_by', 'created_by_name']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class CampaignBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignBooking
        fields = ['id', 'patient', 'campaign', 'booked_at']
        read_only_fields = ['id', 'booked_at', 'patient']

    def validate_patient(self, value):
        if not value.groups.filter(name='Patient').exists():
            raise serializers.ValidationError("Only users with Patient role can be assigned.")
        return value

    def create(self, validated_data):
        validated_data['patient'] = self.context['request'].user
        return super().create(validated_data)



class CampaignReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignReview
        fields = '__all__'
        read_only_fields = ('id','patient',)

    def validate(self, attrs):
        patient = self.context['request'].user
        campaign = attrs.get('campaign')
        if not campaign.bookings.filter(patient=patient).exists():
            raise serializers.ValidationError("You can only review campaigns you have booked.")
        return attrs

    def create(self, validated_data):
        validated_data['patient'] = self.context['request'].user
        return super().create(validated_data)
