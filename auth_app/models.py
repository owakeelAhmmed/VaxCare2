from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from cloudinary.models import CloudinaryField


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('ADMIN', 'Admin')
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PATIENT')
    nid = models.CharField(max_length=20, null=True, blank=True)
    medical_details = models.TextField(blank=True, null=True)
    vaccination_history = models.TextField(blank=True, null=True)
    specialization = models.CharField(max_length=50, blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    # profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    profile_picture = CloudinaryField('profile_picture', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.role == 'PATIENT' and not self.nid and not self.is_superuser:
            raise ValueError("NID is required for patients.")
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nid'],
                condition=Q(role='PATIENT'),
                name='unique_patient_nid'
            )
        ]

    def __str__(self):
        return f"{self.username} ({self.role})"