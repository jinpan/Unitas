from django.contrib import admin

from core.models import Doctor
from core.models import Event
from core.models import EventType
from core.models import FamilyMember
from core.models import Location
from core.models import Nurse
from core.models import Patient

admin.site.register(Patient)
admin.site.register(FamilyMember)
admin.site.register(Doctor)
admin.site.register(Nurse)

admin.site.register(Event)
admin.site.register(EventType)

admin.site.register(Location)

