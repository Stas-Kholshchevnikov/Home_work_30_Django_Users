import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category, Ad
from users.models import User


def start_page(request):
    return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = Category
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        new_category = Category.objects.create(name=data.get("name"))
        return JsonResponse({"id": new_category.id, "name": new_category.name})


class CatListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return JsonResponse([{"id": item.id, "name": item.name} for item in self.object_list.order_by("name")], safe=False)


class CatDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        result = self.get_object()
        return JsonResponse({"id": result.id, "name": result.name})


@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Category
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data.get("name")
        self.object.save()
        return JsonResponse({"id": self.object.id, "name": self.object.name})


@method_decorator(csrf_exempt, name='dispatch')
class CatDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=204)


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


class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by("-price")
        paginator = Paginator(self.object_list, 10)
        page_num = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_num)
        return JsonResponse({"total": page_obj.paginator.count,
                             "num_pages": page_obj.paginator.num_pages,
                             "items": [{"id": item.id,
                                        "name": item.name,
                                        "author": item.author.username,
                                        "price": item.price} for item in page_obj]}, safe=False)


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
