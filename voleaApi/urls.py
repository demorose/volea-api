from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path(r'auth/', include('dj_rest_auth.urls')),
    path(r'auth/registration/', include('dj_rest_auth.registration.urls')),
    path('', include(router.urls)),
]