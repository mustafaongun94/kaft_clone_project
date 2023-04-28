from django import forms
from .models import Carousel, Page

class CarouselModelForm(forms.ModelForm):
    class Meta:
        model = Carousel
        fields = '__all__'
        

class PageModelForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title',
                  'slug',
                  'content',
                  'cover_image',
        ]