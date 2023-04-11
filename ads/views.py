
from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import  UpdateView
from rest_framework.generics import ListAPIView, DestroyAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad, Selection
from ads.permissions import IsOwner, IsStaff
from ads.serializers import AdListSerializer, CategorySerializer, AdDeleteSerializer, AdCreateSerializer, \
    AdUpdateSerializer, SelectionSerializer, SelectionListSerializer, SelectionCreateSerializer, \
    SelectionDetailSerializer



def start_page(request):
    return JsonResponse({"status": "ok"})


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # Оформление суриализаторов и пермишинов для отдельного View во ViewSet
    # default_serializaer_class = CategorySerializer
    # default_permission = [AllowAny]
    #
    # permission = {
    #     "retrive": [IsAuthenticated]
    # }
    # seriazilers = {
    #     "list": CategoryListSerializer,
    #     "retrive": CategoryDetailSerializer
    # }
    #
    # def get_serializer_class(self):
    #     return self.seriazilers.get(self.action, self.default_serializaer_class)
    #
    # def get_permissions(self):
    #     return [permission() for permission in self.permission.get(self.action, self.default_permission)]


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


class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsStaff]


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDeleteSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsStaff]


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


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer
    permission_classes = [IsAuthenticated]


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all()
    default_serializer_class = SelectionSerializer
    default_permission = [AllowAny]

    permission = {
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsOwner],
        "partial_update": [IsAuthenticated, IsOwner],
        "destroy": [IsAuthenticated, IsOwner]
    }
    seriazilers = {
        "list": SelectionListSerializer,
        "create": SelectionCreateSerializer,
        "retrieve": SelectionDetailSerializer
    }

    def get_serializer_class(self):
        return self.seriazilers.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return [permission() for permission in self.permission.get(self.action, self.default_permission)]
