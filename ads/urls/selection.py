
from rest_framework import routers

from ads.views import SelectionViewSet

router_sel = routers.SimpleRouter()
router_sel.register('', SelectionViewSet)

urlpatterns = []
urlpatterns += router_sel.urls
