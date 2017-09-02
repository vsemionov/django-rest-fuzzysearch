from django.conf.urls import url, include
from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.include_format_suffixes = False
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
