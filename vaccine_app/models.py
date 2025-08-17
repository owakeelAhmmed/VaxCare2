from django.db import models
from django.conf import settings
from datetime import timedelta
# Create your models here.


class Vaccine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='vaccines_created')

    def __str__(self):
        return self.name


class VaccineSchedule(models.Model):
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE, related_name='schedules')
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name="schedules")
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.vaccine.name} - {self.date} at {self.location}"


# class DoseBooking(models.Model):
#     patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dose_bookings")
#     schedule = models.ForeignKey(VaccineSchedule, on_delete=models.CASCADE, related_name="bookings")
#     first_dose_date = models.DateField()
#     second_dose_date = models.DateField()
#     booked_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         if not self.second_dose_date:
#             self.second_dose_date = self.first_dose_date + timedelta(days=28)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.patient} - {self.schedule.vaccine.name}"







class DoseBooking(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    schedule = models.ForeignKey('VaccineSchedule', on_delete=models.CASCADE)
    first_dose_date = models.DateField(blank=True, null=True)
    second_dose_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.first_dose_date and self.schedule:
            self.first_dose_date = self.schedule.date

        if not self.second_dose_date and self.first_dose_date:
            self.second_dose_date = self.first_dose_date + timedelta(days=28)

        super().save(*args, **kwargs)

        if self.schedule and hasattr(self.schedule, 'campaign'):
            CampaignBooking.objects.get_or_create(
                patient=self.patient,
                campaign=self.schedule.campaign
            )

# class Campaign(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     start_date = models.DateField()
#     end_date = models.DateField()
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name


class Campaign(models.Model):
    name = models.CharField(max_length=255)
    vaccine_type = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name="campaigns")
    start_date = models.DateField()
    end_date = models.DateField()
    dose_interval_days = models.PositiveIntegerField(help_text="Interval in days between doses")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="campaigns_created"
    )

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-start_date']




class CampaignBooking(models.Model):
     patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='campaign_bookings')
     campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='bookings')
     booked_at = models.DateTimeField(auto_now_add=True)

class CampaignReview(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='campaign_reviews')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('patient', 'campaign')

    def __str__(self):
        return f"Review by {self.patient} on {self.campaign}"