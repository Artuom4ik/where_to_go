from django.shortcuts import render
from .models import Place
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse

# Create your views here.


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


def get_images(place):
    images = place.images.all()
    images_url = []
    for image in images:
        images_url.append(image.image.url)
    return images_url


def place_detail_show(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    place_description = {
        "title": place.title,
        "imgs": get_images(place),
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": place.longitude,
            "lat": place.latitude
        }
    }
    return JsonResponse(place_description, json_dumps_params={'ensure_ascii': False, 'indent': 2})
