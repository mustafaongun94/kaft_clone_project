from django.shortcuts import (
    render, 
    redirect, 
    get_object_or_404, #object'i getirir veya 404 hatası verir
    )
from django.contrib import messages
from .models import Carousel, Page
from .forms import CarouselModelForm, PageModelForm
from django.utils.text  import slugify
from product.models import Product

STATUS = 'published'


def index(request):
    context = dict()
    context['images'] = Carousel.objects.filter(
        status=STATUS
        ).exclude(cover_image = '')
    products = Product.objects.filter(
        is_home=True,
        status = STATUS              
                                    )
    context['products'] = products
    
    return render(request,'home/index.html',context)


def page_show(request, slug):
    context = dict()
    context['page'] = get_object_or_404(Page, slug=slug)
    return render(request, 'page/page.html', context)


def manage_list(request):
    context = dict()
    return render(request, 'manage/manage.html',context)


def page_list(request):
    context = dict()
    context['items'] = Page.objects.all()
    return render(request,'manage/page_list.html',context)


def page_create(request):
    context = dict()
    context['title'] = 'Page Create Form'
    context['form']  = PageModelForm()
    if request.method == 'POST':
        form = PageModelForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.slug = slugify(item.title.replace('ı','i'))
        messages.success(request,'Bişiler eklendi')
    return render(request, 'manage/form.html',context)


def page_update(request, pk):
    context = dict()
    item = Page.objects.get(pk=pk)
    context['title'] = f"{item.title} - {item.pk} Carousel Create Form"
    context['form'] = PageModelForm(instance = item)
    if request.method == POST:
        form = PageModelForm(request.POST, request.FILES, instance = item)
        if form.is_valid():
            item = form.save(commit=True)
            if item.slug == '':
                item.slug = slugify(item.title.replace('ı','i'))
            item.save()
            return redirect('page_update',pk)
    return render(request,'manage/form.html',context)


def page_delete(request,pk):
    item = Page.objects.get(pk = pk)
    item.status = 'deleted'
    item.save()
    return redirect('page_list')


def carousel_list(request):
    context = dict()
    context['carousel'] = Carousel.objects.all()
    return render(request,'manage/carousel_list.html',context)


def carousel_update(request, pk):
    context = dict()
    item = Carousel.objects.get(pk=pk)
    context['title'] = f"{item.title} - {item.pk} Carousel Create Form"
    context['form'] = CarouselModelForm(instance = item)
    if request.method == POST:
        form = CarouselModelForm(request.POST, request.FILES, instance = item)
        if form.is_valid():
            form.save()
            return redirect('carousel_update',pk)
    return render(request,'manage/form.html',context)


def carousel_create(request):
    context = dict()
    context['title'] = 'Carousel Create Form'
    context['form']  = CarouselModelForm()
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES.get('cover_image'))
        form = CarouselModelForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
        messages.success(request,'Bişiler eklendi')
    return render(request, 'manage/form.html',context)
