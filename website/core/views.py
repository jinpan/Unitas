from json import dumps
import datetime

from django.shortcuts import render
from django.http import HttpResponse

from core.models import Location
from core.models import Event

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

    events = Event.objects.filter(starttime__lte=end_dt, endtime__gte=start_dt, patient__pk=p_id)

    return JSONResponse([event.to_dict() for event in events])

