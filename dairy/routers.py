from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'dairy', views.DairyViewSet, base_name='dairy')
