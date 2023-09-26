import json
import logging

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from places.models import Place, Image


logger = logging.getLogger('load_place')


class Command(BaseCommand):
    help = 'Adds the specified location to the database.'

    def add_arguments(self, parser):
        parser.add_argument('--path', '-p')
        parser.add_argument('--json_url', '-url')
        parser.add_argument('--urls_path', '-urls')

    def handle(self, *args, **options):
        if options['path'] or options['json_url']:
            self.load_place(options['path'], options['json_url'])
        else:
            self.load_places(options['urls_path'])

    def load_places(self, urls_path):
        with open(urls_path, 'r', encoding='UTF8') as file:
            json_urls = json.load(file)

        for json_url in json_urls['places']:
            try:
                self.load_place(path=False, json_url=json_url)
            except requests.exceptions.InvalidSchema as url_error:
                logger.error(url_error)
                continue

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
            short_description=place_file['description_short'],
            long_description=place_file['description_long'],
            latitude = place_file['coordinates']['lat'],
            longitude = place_file['coordinates']['lng']
        )
        
        for number, image_url in enumerate(place_file['imgs']):
            try:
                response = requests.get(image_url)
                response.raise_for_status()
                image_name = f'{place.title}_{number}.jpg'
                Image.objects.update_or_create(
                    place=place,
                    image=ContentFile(name=image_name, content=response.content),
                    image_number=number
                )
            except (requests.exceptions.HTTPError, requests.exceptions.ReadTimeout):
                logger.warning(f"Картинка места {place.title}, под номером {number} не скачалась.")
                


