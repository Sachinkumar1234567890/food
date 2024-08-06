from django.db import models
from accounts.models import User,UserProfile
from datetime import time

# Create your models here.

class Vendor(models.Model):
    user=models.OneToOneField(User,related_name='user', on_delete=models.CASCADE, blank=True, null=True)
    userprofile=models.OneToOneField(UserProfile,related_name='userprofile',on_delete=models.CASCADE,blank=True, null=True)
    restaurant_name=models.CharField(max_length=250, blank=True, null=True)
    restaurant_license=models.ImageField(upload_to='license')
    is_approved=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.restaurant_name
    

class Opening_Hours(models.Model):
    DAYS=[
        ('1','SUNDAY'),
        ('2','MONDAY'),
        ('3','TUESDAY'),
        ('4','WEDNESDAY'),
        ('5','THURSDAY'),
        ('6','FRIDAY'),
        ('7','SATURDAY'),

    ]
    TIMING=[(time(h, m).strftime('%I:%M %p'),time(h, m).strftime('%I:%M %p')) for h in range(0,24) for m in (0,30)]
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    days = models.CharField(choices=DAYS,max_length=10)
    open_time = models.CharField(choices=TIMING,max_length=100)
    close_time = models.CharField(choices=TIMING,max_length=100)
    is_opened = models.BooleanField(default=False)

    def __str__(self):
        return self.days

    def get_day(self):
        if self.days == "1":
            select_days = "SUNDAY"
        elif self.days == "2":
            select_days = "MONDAY"
        elif self.days == "3":
            select_days = "TUESDAY"
        elif self.days == "4":
            select_days = "WEDNESDAY"
        elif self.days == "5":
            select_days = "THURSDAY"
        elif self.days == "6":
            select_days = "FRIDAY"
        elif self.days == "7":
            select_days = "SATURDAY"
        return select_days





