from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = HTMLField()
    dnt = models.DateTimeField()
    venue = models.CharField(max_length=50)
    total_seats = models.IntegerField()
    organizer = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True)
    
    @property
    def seats(self):
        total = self.total_seats
        taken = self.bookings.all().count()
        return total - taken
    
    def __str__(self):
        return self.name


class Bookings(models.Model):
    event = models.ForeignKey(Event,
                            on_delete=models.SET_NULL,
                            null= True, 
                            blank = True,
                            related_name="bookings")
    participant = models.ForeignKey(User,
                            on_delete=models.SET_NULL,
                            null= True, 
                            blank = True,
                            related_name="bookings")
    booked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return self.participant.username + self.event.name


    


class ExpiredEvent(Event):

    class Meta:
        proxy = True
        verbose_name = "Expired Event"
        verbose_name_plural = "Expired Events"