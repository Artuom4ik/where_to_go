from django.shortcuts import render
from .models import Place

# Create your views here.


def index(request):
    places = Place.objects.all()
    places_description = []
    for place in places:
        places_description.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.longitude, place.latitude]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": "./static/places/moscow_legends.json"
            }
            }
        )
    context = {
        "places": {
            "type": "FeatureCollection",
            "features": places_description
        }
    }
    return render(request, 'index.html', context)
