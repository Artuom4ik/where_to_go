from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from django.utils.html import format_html

from .models import Place, Image

# Register your models here.
class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    ordering = ['image_number']
    readonly_fields = ["headshot_image"]
    fields = ('image', 'headshot_image', 'image_number',)

    def headshot_image(self, obj):
        return format_html(f'<img src="{obj.image.url}" style="max-height: 200px; max-width: 200px;" >')


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_filter = ('place',)
