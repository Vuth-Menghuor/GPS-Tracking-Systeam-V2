from django.db import models
from django.utils import timezone

# Create your models here.

class DeviceData(models.Model):
    ranking_id = models.AutoField(primary_key=True)  # Custom primary key for ranking
    imei = models.CharField(max_length=20, unique=True)  # IMEI numbers are usually 15 digits
    latitude = models.DecimalField(max_digits=9, decimal_places=6)   # precise for GPS
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    coordinates = models.CharField(max_length=50)  # storing as string "lat,long"
    
    datastatus = models.IntegerField()  
    datastatus_description = models.CharField(max_length=50)
    
    hearttime_date = models.DateField(null=True, blank=True)
    hearttime_time = models.TimeField(null=True, blank=True)
    hearttime_unix = models.BigIntegerField()  # Unix timestamp
    
    status = models.CharField(max_length=20)

    # Detailed timestamp used by imports and ranking; keep non-null for integrity
    last_update_detailed_db = models.DateTimeField(default=timezone.now)

    # Relative timestamp (keeps existing DB compatibility). Add as non-null with a default
    # to satisfy older rows that expect this column.
    last_update_relative_db = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)  # optional, track when saved
    updated_at = models.DateTimeField(auto_now=True)      # optional, track updates

    class Meta:
        ordering = ['ranking_id']

    def __str__(self):
        return f"IMEI: {self.imei} - {self.status}"
