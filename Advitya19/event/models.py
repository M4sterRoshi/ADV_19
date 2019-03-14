from django.db import models
from user.models import User

class Organizer(models.Model):
    name = models.CharField(max_length=100)
    logo = models.CharField(max_length=100)

    def __str__(self):
        return(self.name)


class Event(models.Model):
    FEST = (
        ('TECH', 'Techfest'),
        ('CULT', 'Cultural Fest'),
        ('SPRT', 'Sports Fest')    
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=6, unique=True)
    time = models.DateTimeField()
    brief_description = models.TextField()
    short_description =  models.TextField()
    poster = models.CharField(max_length=100)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    def __str__(self):
        return(self.code + self.name)

class Coordinator(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    contact_num = models.CharField(max_length=10)

    def __str__(self):
        return(self.name)


class RegistrationManager(models.Manager):
    use_in_migrations = True

    def create_registration(self, event, user):
        registration = self.model(
            event=event,
            user=user,
        )
        registration.save(using=self._db)
        return registration

class Registration(models.Model):
    is_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user  = models.ForeignKey(User,  on_delete=models.CASCADE)
    paymentID = models.CharField(max_length=100, blank=True, default=False)
    objects = RegistrationManager()

    def __str__(self):
        if self.is_paid:
            return str(self.event) + " - " + str(self.user) + " - PAID" 
        else:
            return str(self.event) + " - " + str(self.user) + " - UNPAID"


class Tag(models.Model):
    name = models.CharField(max_length=20)
    event = models.ManyToManyField(Event)

    def __str__(self):
        return(self.name)

