from json import dumps
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse

from core.models import Location
from core.models import Event
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
def get_locations(request):

    locations = []
    for location in Location.objects.all():
        locations.append(location.to_dict())

    return JSONResponse(locations)

@login_required(login_url='/accounts/login2')
def get_events(request):
    # request will contain patient id, date
    p_id = request.GET.get('patient_id')
    date = request.GET.get('date')
    if p_id is None or date is None:
        return JSONResponse([])

    start_dt = datetime.datetime.strptime(date, '%m/%d/%Y')
    end_dt = start_dt + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)

    events = Event.objects.filter(starttime__lte=end_dt, endtime__gte=start_dt, patient__pk=p_id)

    return JSONResponse([event.to_dict() for event in events])

