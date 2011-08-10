import json

from django.core import serializers
from django.http import HttpResponse

from decorators import json_view
from iphonefood_core.models import Dish, Address


def dishes(request):
    data = Dish.objects.all().values('category__name', 'name', 'price', 'rating', 'description', 'photo_url')
    return HttpResponse(json.dumps(list(data),sort_keys=True, indent=4, ensure_ascii=False), mimetype='application/json')


def top(request):
    data = (Dish.objects.exclude(rating=0)\
        .order_by('-rating')
        .values('category__name', 'name', 'price', 'rating', 'description', 'photo_url'))
    return HttpResponse(json.dumps(list(data),sort_keys=True, indent=4, ensure_ascii=False), mimetype='application/json')


def addresses(request):
    data = Address.objects.all().values('city', 'district', 'address', 'description')
    return HttpResponse(json.dumps(list(data),sort_keys=True, indent=4, ensure_ascii=False), mimetype='application/json')

