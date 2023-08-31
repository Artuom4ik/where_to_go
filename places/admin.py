from django.contrib import admin
from adminsortable2.admin import SortableStackedInline
from django.utils.html import format_html

from .models import Place, Image

# Register your models here.
class ImageInline(admin.TabularInline):
    model = Image
    readonly_fields = ["headshot_image"]
    fields = ('image', 'headshot_image', 'image_number',)

    def headshot_image(self, obj):
        return format_html(f'<img src="{obj.image.url}" style="max-height: 200px; max-width: 200px;" >')


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
