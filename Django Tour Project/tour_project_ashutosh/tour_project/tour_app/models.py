from django.db import models
from django.contrib.auth.models import User
import random
import uuid
from django.utils import timezone
# Create your models here.


class Places(models.Model):
    place_name=models.CharField(max_length=500,blank=True,null=False)
    seat_counts=models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.place_name

class packages(models.Model):
    from_place=models.ManyToManyField(Places,blank=True,null=True)
    package_id=models.AutoField(primary_key=True)
    p1_img=models.ImageField(upload_to='placess/')
    p1_name=models.CharField(max_length=50)
    p1_price=models.IntegerField(default=0)
    trending=models.BooleanField(default=False)
    seats=models.CharField(max_length=50,default=50)
    is_pack_available=models.BooleanField(default=True)
    def __str__(self):
        return str(self.package_id)
    
    
class user_booking(models.Model):
    typeofuser=(
        ('Adults','Adult'),
        ('child','child')
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    user_img=models.ImageField(upload_to='userimg/',default=False)
    package_id=models.ForeignKey(packages,on_delete=models.DO_NOTHING)
    from_place=models.ForeignKey(Places,on_delete=models.CASCADE,blank=True,null=True)
    travel_date=models.DateField(blank=True,null=True)
    booking_id=models.UUIDField(default=uuid.uuid4, unique=True)
    name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=50,blank=True,null=True)
    type=models.CharField(choices=typeofuser,max_length=50)
    Adult_price=models.IntegerField(default=0)
    child_price=models.IntegerField(default=0)
    seat_no=models.CharField(max_length=50,default=0)
    confirm=models.BooleanField(default=False)
    payment=models.BooleanField(default=False)
    payment_id=models.CharField(max_length=50,default=0)
    ticket_expair=models.BooleanField(default=False)

    def save(self, *args, **kwargs):
    # Call the original save method to handle the instance itself
        super().save(*args, **kwargs)
        # Get the current local date
        now = timezone.localdate()
        # Filter objects with ticket_expair=False and check if travel_date has passed
        objs = user_booking.objects.filter(ticket_expair=False)
        for i in objs:
            # Check if the current date is past the travel_date
            if i.travel_date and now < i.travel_date:  # Ensure that travel_date is compared as a date
                i.ticket_expair = True
                i.save()  # Save 


    def __str__(self):
        return str(self.package_id)


