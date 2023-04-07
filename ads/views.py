import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad
from ads.serializers import AdListSerializer, CategorySerializer
from users.models import User


def start_page(request):
    return JsonResponse({"status": "ok"})


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AdListView(ListAPIView):
    queryset = Ad.objects.all().order_by("-price")
    serializer_class = AdListSerializer

    def list(self, request, *args, **kwargs):

        category = request.GET.get("cat")
        if category:
            self.queryset = self.queryset.filter(category_id__in=category)

        text = request.GET.get("text")
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get("location")
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = request.GET.get("price_from")
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get("price_to")
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        author = get_object_or_404(User, pk=data.pop("author_id"))
        category = get_object_or_404(Category, pk=data.pop("category_id"))
        new_ad = Ad.objects.create(author=author, category=category, **data)
        return JsonResponse({"id": new_ad.id,
                             "name": new_ad.name,
                             "author": new_ad.author.username,
                             "price": new_ad.price,
                             "description": new_ad.description,
                             "address": [loc.name for loc in new_ad.author.location.all()],
                             "is_published": new_ad.is_published,
                             "category": new_ad.category.name})


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if 'name' in data:
            self.object.name = data.get("name")
        if 'price' in data:
            self.object.price = data.get("price")
        if 'description' in data:
            self.object.description = data.get("description")
        if 'author' in data:
            author = get_object_or_404(User, pk=data.get("author_id"))
            self.object.author = author
        if 'category' in data:
            category = get_object_or_404(Category, pk=data.get("category_id"))
            self.object.category = category
        self.object.save()

        return JsonResponse({"id": self.object.id,
                             "name": self.object.name,
                             "author": self.object.author.username,
                             "price": self.object.price,
                             "description": self.object.description,
                             "address": [loc.name for loc in self.object.author.location.all()],
                             "is_published": self.object.is_published,
                             "category": self.object.category.name})


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image")
        self.object.save()
        return JsonResponse({"id": self.object.id,
                             "name": self.object.name,
                             "author": self.object.author.username,
                             "price": self.object.price,
                             "description": self.object.description,
                             "address": [loc.name for loc in self.object.author.location.all()],
                             "is_published": self.object.is_published,
                             "category": self.object.category.name,
                             "image": self.object.image.url})


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        result = self.get_object()
        return JsonResponse({"id": result.id,
                             "name": result.name,
                             "author": result.author.username,
                             "price": result.price,
                             "description": result.description,
                             "address": [loc.name for loc in result.author.location.all()],
                             "is_published": result.is_published,
                             "category": result.category.name,
                             "image": result.image.url})
