import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Category, Ad


def start_page(request):
    return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):

    def get(self, request):
        result = Category.objects.all()
        return JsonResponse([{"id": item.id, "name": item.name} for item in result], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        new_category = Category.objects.create(name=data.get("name"))
        return JsonResponse({"id": new_category.id, "name": new_category.name})


@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):

    def get(self, request):
        result = Ad.objects.all()
        return JsonResponse([{"id": item.id,
                             "name": item.name,
                             "author": item.author,
                             "price": item.price} for item in result], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        new_ad = Ad.objects.create(**data)
        return JsonResponse({"id": new_ad.id,
                             "name": new_ad.name,
                             "author": new_ad.author,
                             "price": new_ad.price,
                             "description": new_ad.description,
                             "address": new_ad.address,
                             "is_published": new_ad.is_published})


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        result = self.get_object()
        return JsonResponse({"id": result.id, "name": result.name})


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        result = self.get_object()
        return JsonResponse({"id": result.id,
                             "name": result.name,
                             "author": result.author,
                             "price": result.price,
                             "description": result.description,
                             "address": result.address,
                             "is_published": result.is_published})
