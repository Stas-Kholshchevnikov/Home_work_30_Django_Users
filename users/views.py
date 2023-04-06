import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from users.models import User, Location


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        location = data.pop("locations")
        new_user = User.objects.create(**data)

        for each_loc in location:
            loc, created = Location.objects.get_or_create(name=each_loc)
            new_user.location.add(loc)

        return JsonResponse({"id": new_user.id,
                            "username": new_user.username,
                            "first_name": new_user.first_name,
                            "last_name": new_user.last_name,
                            "role": new_user.role,
                            "locations": [loc.name for loc in new_user.location.all()],
                            "age": new_user.age})


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if 'username' in data:
            self.object.username = data.get("username")
        if 'first_name' in data:
            self.object.first_name = data.get("first_name")
        if 'last_name' in data:
            self.object.last_name = data.get("last_name")
        if 'role' in data:
            self.object.role = data.get("role")
        if 'locations' in data:
            self.object.location.clear()
            for each_loc in data.get("locations"):
                loc, created = Location.objects.get_or_create(name=each_loc)
                self.object.location.add(loc)
        if 'age' in data:
            self.object.age = data.get("age")
        self.object.save()

        return JsonResponse({"id": self.object.id,
                            "username": self.object.username,
                            "first_name": self.object.first_name,
                            "last_name": self.object.last_name,
                            "role": self.object.role,
                            "locations": [loc.name for loc in self.object.location.all()],
                            "age": self.object.age})


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=204)


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.annotate(total_ads=Count("ad", filter=Q(ad__is_published=True)))
        paginator = Paginator(self.object_list, 10)
        page_num = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_num)
        return JsonResponse({"total": page_obj.paginator.count,
                             "num_pages": page_obj.paginator.num_pages,
                             "items": [{"id": item.id,
                                        "username": item.username,
                                        "first_name": item.first_name,
                                        "last_name": item.last_name,
                                        "role": item.role,
                                        "locations": [loc.name for loc in item.location.all()],
                                        "age": item.age,
                                        "total_ads": item.total_ads} for item in page_obj]}, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        result = self.get_object()
        return JsonResponse({"id": result.id,
                             "username": result.username,
                             "first_name": result.first_name,
                             "last_name": result.last_name,
                             "role": result.role,
                             "locations": [loc.name for loc in result.location.all()],
                             "age": result.age})
