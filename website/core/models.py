from django.contrib.auth.models import User
from django.db import models


class Patient(models.Model):

    SSN = models.CharField(max_length=9)

    doctors = models.ManyToManyField('Doctor')
    nurses = models.ManyToManyField('Nurse')

    checkin = models.DateTimeField()
    checkout = models.DateTimeField(null=True, blank=True)

    description = models.TextField()
    location = models.ForeignKey('Location')


class Doctor(models.Model):

    user = models.OneToOneField(User)


class Nurse(models.Model):

    user = models.OneToOneField(User)


class FamilyMember(models.Model):

    user = models.OneToOneField(User)

    patient = models.ForeignKey('Patient')

    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=10)


class Event(models.Model):

    datetime = models.DateTimeField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    notes = models.TextField(null=True, blank=True)
    flagged = models.BooleanField(default=False)
    event_type = models.ForeignKey('EventType')
    location = models.ForeignKey('Location')

    patient = models.ForeignKey('Patient')


class EventType(models.Model):

    name = models.CharField(max_length=100)
    # color is 6 char hex code
    color = models.CharField(max_length=6)


class Location(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()

