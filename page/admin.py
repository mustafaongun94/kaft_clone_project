from django.contrib import admin
from .models import Page, Carousel


class PageAdmin(admin.ModelAdmin):
  list_display = (
    'pk',
    'title',
    'status',
    'updated_at'
    )
  prepopulated_fields = {"slug": ("title",)}


class CarouselAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'title',
        'cover_image',
        'status',
    ]
    list_filter = ['status', ]
    list_editable = list_filter


admin.site.register(Page, PageAdmin)
admin.site.register(Carousel, CarouselAdmin)