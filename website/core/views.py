from json import dumps
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse

from core.models import Doctor
from core.models import Event
from core.models import Location
from core.models import Nurse
from core.models import Patient

def login(request):
    ssn = request.POST.get('ssn')

    if ssn and Patient.objects.filter(SSN=ssn):
        patient = Patient.objects.get(SSN=ssn)
        user = patient.user
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, user)
        return redirect('get_events')

    return render(request, 'registration/login2.html')


def JSONResponse(data):
    return HttpResponse(dumps(data), content_type='application/json')


@login_required
def add_event(request):
    if (Doctor.objects.filter(user=request.user)
            or Nurse.objects.filter(user=request.user)):
        return render(request, 'add_event.html')
    else:
        raise Http404


@login_required
def get_locations(request):

    locations = []
    for location in Location.objects.all():
        locations.append(location.to_dict())

    return JSONResponse(locations)

def get_doctors(request):

    doctors = []
    for doctor in Doctor.objects.all():
        doctors.append(doctor.to_dict())

    return JSONResponse(doctors)

def get_nurses(request):

    nurses = []
    for nurse in Nurse.objects.all():
        nurses.append(nurse.to_dict())

    return JSONResponse(nurses)

@login_required(login_url='/accounts/login2')
def get_events(request):
    # request will contain date if patient; date and patient id if nurse/doctor
    p_id = request.GET.get('patient_id')
    if p_id is None:
        patients = Patient.objects.filter(user=request.user)
        if patients:
            p_id = patients[0].pk
    date = request.GET.get('date')
    if p_id is None or date is None:
        return JSONResponse([])

    start_dt = datetime.datetime.strptime(date, '%m/%d/%Y')
    end_dt = start_dt + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)

    events = Event.objects.filter(starttime__lte=end_dt, endtime__gte=start_dt, patient__pk=p_id).order_by('starttime')

    return JSONResponse([event.to_dict() for event in events])

def get_patients(request):
    # request will contain either doctor id or nurse id
    d_id = request.GET.get('doctor_id')
    n_id = request.GET.get('nurse_id')
    patients = []

    if d_id is not None:
        patients = Patient.objects.filter(doctors=Doctor.objects.get(pk=d_id)).order_by('user__last_name')
    elif n_id is not None:
        patients = Patient.objects.filter(nurses=Nurse.objects.get(pk=n_id)).order_by('user__last_name')
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

@login_required(login_url='/accounts/login2')
def patient_view(request):
    return render(request, 'patients.html')
