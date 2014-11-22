from json import dumps

from django.shortcuts import render
from django.http import HttpResponse

from core.models import Location


def JSONResponse(data):
    return HttpResponse(dumps(data), content_type='application/json')


def get_locations(request):

    locations = []
    for location in Location.objects.all():
        locations.append(location.to_dict())

    return JSONResponse(locations)

