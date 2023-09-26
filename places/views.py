import logging

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse

from .models import Place


logger = logging.getLogger(__name__)


def index(request):
    places = Place.objects.all()
    context = {
        "places": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [place.longitude, place.latitude]
                    },
                    "properties": {
                        "title": place.title,
                        "placeId": place.id,
                        "detailsUrl": reverse('place_description', args=[place.id])
                    }
                } for place in places
            ]
        }
    }
    return render(request, 'index.html', context)


def place_detail_show(request, place_id):
    place = get_object_or_404(Place.objects.prefetch_related('images'), id=place_id)
    place_description = {
        "title": place.title,
        "imgs": [image.image.url for image in place.images.all()],
        "description_short": place.short_description,
        "description_long": place.long_description,
        "coordinates": {
            "lng": place.longitude,
            "lat": place.latitude
        }
    }
    return JsonResponse(place_description, json_dumps_params={'ensure_ascii': False, 'indent': 2})
