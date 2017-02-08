from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'operate', views.OperateViewSet, base_name='operate')
