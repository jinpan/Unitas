from random import randint

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models


class Patient(models.Model):
    user = models.OneToOneField(User)

    SSN = models.CharField(max_length=9, unique=True)

    doctors = models.ManyToManyField('Doctor')
    nurses = models.ManyToManyField('Nurse')

    checkin = models.DateTimeField()
    checkout = models.DateTimeField(null=True, blank=True)

    description = models.TextField()
    location = models.ForeignKey('Location')

    def __unicode__(self):
        name = self.user.get_full_name() or self.user.get_username()
        return u'<Patient %s>' % name

    def to_dict(self):
        obj = {
            'id': self.pk,
            'name': self.user.get_full_name(),
        }
        return obj


class Doctor(models.Model):

    user = models.OneToOneField(User)

    def __unicode__(self):
        name = self.user.get_full_name() or self.user.get_username()
        return u'<Doctor %s>' % name


class Nurse(models.Model):

    user = models.OneToOneField(User)

    def __unicode__(self):
        name = self.user.get_full_name() or self.user.get_username()
        return u'<Nurse %s>' % name


class FamilyMemberManager(models.Manager):

    def create_fm(self, first_name, last_name, email, phone, patient):
        username = '%09d' % randint(0, 999999999)
        while User.objects.filter(username=username):
            username = '%09d' % randint(0, 999999999)

        password = '%06d' % randint(0, 999999)
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.password = make_password(password)
        user.save()

        familymember = FamilyMember(
            user=user,
            patient=patient,
            email=email,
            phone=phone
        )
        familymember.save()

        send_mail(
            "Unitas Invite",
            """Your username is %s, and your pin number has been sent to your phone.""" % username,
            'teamkatedonthate@gmail.com',
            [email],
        )
        send_mail(
            "Unitas PIN code",
            'Your pin code is %s' % password,
            'teamkatedonthate@gmail.com',
            ['%s@txt.att.net' % phone],
        )

        # send an email to give the family member the url/username
        # send a text message for 2FA pin

        return familymember


class FamilyMember(models.Model):

    user = models.OneToOneField(User)

    patient = models.ForeignKey('Patient')

    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=10)

    objects = FamilyMemberManager()
    def __unicode__(self):
        name = self.user.get_full_name() or self.user.get_username()
        return u'<Family Member %s>' % name


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

    def to_dict(self):
        obj = {
            'id': self.pk,
            'starttime': str(self.starttime),
            'endtime': str(self.endtime),
            'duration': (self.endtime - self.starttime).seconds,
            'name': self.name,
            'description': self.description,
            'notes': self.notes,
            'flagged': self.flagged,
            'event_type': self.event_type.to_dict(),
            'location': self.location.to_dict(),
            'patient': self.patient.to_dict(),
        }
        return obj

    def set_flagged(self, bool):
        self.flagged = bool
        self.save()

class EventType(models.Model):

    name = models.CharField(max_length=100)
    # color is 6 char hex code
    color = models.CharField(max_length=6)

    def __unicode__(self):
        return u'<Event Type %s>' % self.name

    def to_dict(self):
        obj = {
            'id': self.pk,
            'name': self.name,
            'color': self.color,
        }
        return obj


class Location(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return u'<Location %s>' % self.name

    def to_dict(self):
        obj = {
            'id': self.pk,
            'name': self.name,
            'description': self.description,
        }

        return obj

