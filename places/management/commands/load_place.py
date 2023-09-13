import json
import os
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

import requests

from places.models import Place, Image


class Command(BaseCommand):
    help = 'Adds the specified location to the database.'

    def add_arguments(self, parser):
        parser.add_argument('--path', '-p')
        parser.add_argument('--json_url', '-url')

    def handle(self, *args, **options):
        if options['path'] or options['json_url']:
            self.load_place(options['path'], options['json_url'])

    def load_place(self, path, json_url):
        if path:
            with open(path, "r", encoding='UTF8') as my_file:
                place_file = json.load(my_file)
        else:
            response = requests.get(json_url)
            response.raise_for_status()
            place_file = response.json()

        place, create = Place.objects.update_or_create(
            title=place_file['title'],
            description_short=place_file['description_short'],
            description_long=place_file['description_long'],
            latitude = place_file['coordinates']['lat'],
            longitude = place_file['coordinates']['lng']
        )
        
        for number, image_url in enumerate(place_file['imgs']):
            response = requests.get(image_url)
            response.raise_for_status()
            image_name = f'{place.title}_{number}.jpg'
            Image.objects.update_or_create(
                place=place,
                image=ContentFile(name=image_name, content=response.content),
                image_number=number
            )
