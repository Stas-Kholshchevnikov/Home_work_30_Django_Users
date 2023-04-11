from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer
from ads.models import Ad, Category, Selection
from users.models import User


class AdListSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field="username", queryset=User.objects.all())
    category = SlugRelatedField(slug_field="name", queryset=Category.objects.all())

    class Meta:
        model = Ad
        fields = '__all__'


class AdDeleteSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateSerializer(ModelSerializer):

    def is_valid(self, *, raise_exception=False):
        self._author_id = self.initial_data.pop('author_id', None)
        self._category_id = self.initial_data.pop('category_id', None)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        author = get_object_or_404(User, pk=self._author_id)
        category = get_object_or_404(Category, pk=self._category_id)
        new_ad = Ad.objects.create(author=author, category=category, **validated_data)
        return new_ad

    class Meta:
        model = Ad
        fields = '__all__'


class AdUpdateSerializer(ModelSerializer):

    def is_valid(self, *, raise_exception=False):
        self._author_id = self.initial_data.pop('author_id', None)
        self._category_id = self.initial_data.pop('category_id', None)
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        author = get_object_or_404(User, pk=self._author_id)
        category = get_object_or_404(Category, pk=self._category_id)
        ad = super().save(author=author, category=category, **kwargs)
        return ad

    class Meta:
        model = Ad
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SelectionSerializer(ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionListSerializer(ModelSerializer):
    owner = SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionDetailSerializer(ModelSerializer):
    items = AdListSerializer(many=True)

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSerializer(ModelSerializer):
    owner = SlugRelatedField(slug_field="username", read_only=True)

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["owner"] = request.user
        return super().create(validated_data)

    class Meta:
        model = Selection
        fields = '__all__'
