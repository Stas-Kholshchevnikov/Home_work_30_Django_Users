
from rest_framework import routers

from ads.views import CategoryViewSet

router_cat = routers.SimpleRouter()
router_cat.register('', CategoryViewSet)

urlpatterns = []
urlpatterns += router_cat.urls
