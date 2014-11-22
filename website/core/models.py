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

    def __unicode__(self):
        return u'<Patient %s>' % self.user.get_full_name()


class Doctor(models.Model):

    user = models.OneToOneField(User)

    def __unicode__(self):
        return u'<Doctor %s>' % self.user.get_full_name()


class Nurse(models.Model):

    user = models.OneToOneField(User)

    def __unicode__(self):
        return u'<Nurse %s>' % self.user.get_full_name()


class FamilyMember(models.Model):

    user = models.OneToOneField(User)

    patient = models.ForeignKey('Patient')

    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=10)

    def __unicode__(self):
        return u'<Family Member %s>' % self.user.get_full_name()


class Event(models.Model):

    starttime = models.DateTimeField()
    endtime = models.DateTimeField()

    name = models.CharField(max_length=100)
    description = models.TextField()
    notes = models.TextField(null=True, blank=True)
    flagged = models.BooleanField(default=False)
    event_type = models.ForeignKey('EventType')
    location = models.ForeignKey('Location')

    patient = models.ForeignKey('Patient')

    def __unicode__(self):
        return u'<Event %s>' % self.name


class EventType(models.Model):

    name = models.CharField(max_length=100)
    # color is 6 char hex code
    color = models.CharField(max_length=6)

    def __unicode__(self):
        return u'<Event Type %s>' % self.name


class Location(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return u'<Location %s>' % self.name

