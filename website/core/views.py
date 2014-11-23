from json import dumps
import datetime

from django.shortcuts import render
from django.http import HttpResponse

from core.models import Doctor
from core.models import Event
from core.models import Location
from core.models import Nurse
from core.models import Patient

def JSONResponse(data):
    return HttpResponse(dumps(data), content_type='application/json')


def get_locations(request):

    locations = []
    for location in Location.objects.all():
        locations.append(location.to_dict())

    return JSONResponse(locations)

def get_events(request):
    # request will contain patient id, date
    p_id = request.GET.get('patient_id')
    date = request.GET.get('date')
    if p_id is None or date is None:
        return JSONResponse([])

    start_dt = datetime.datetime.strptime(date, '%m/%d/%Y')
    end_dt = start_dt + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)
    print start_dt, end_dt

    events = Event.objects.filter(starttime__lte=end_dt, endtime__gte=start_dt, patient__pk=p_id).order_by('starttime')

    return JSONResponse([event.to_dict() for event in events])

def get_patients(request):
    # request will contain either doctor id or nurse id
    d_id = request.GET.get('doctor_id')
    n_id = request.GET.get('nurse_id')
    patients = []

    if d_id is not None:
        patients = Patient.objects.filter(doctors=Doctor.objects.get(pk=d_id))
    elif n_id is not None:
        patients = Patient.objects.filter(nurses=Nurse.objects.get(pk=n_id))
    else:
        patients = []

    return JSONResponse([patient.to_dict() for patient in patients])

def flag_on(request):
    # request will contain event id
    e_id = request.GET.get('event_id')
    event = Event.objects.get(pk=e_id)
    event.set_flag(True)
    return HttpResponse('')

def flag_off(request):
    # request will contain event id
    e_id = request.GET.get('event_id')
    event = Event.objects.get(pk=e_id)
    event.set_flag(False)
    return HttpResponse('')
