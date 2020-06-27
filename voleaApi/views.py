from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets
from .models import Item, Profile, Category
from .serializers import ItemSerializer, CategorySerializer, VoleaUserDetailsSerializer
from .permissions import IsOwnerOrReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    filterset_fields = ['name']
    serializer_class = ItemSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated is False:
            return Category.objects.filter(owner__profile__isPublic = True)
        elif self.request.user.is_superuser:
            return Category.objects.all()
        else:
            return Category.objects.filter(
                Q(owner__isPublic = True) |
                Q(owner__share_with__id = self.request.user.id) |
                Q(owner__id = self.request.user.id)
            )

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user) 
    
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    filterset_fields = ['name', 'owner__id']
    serializer_class = ItemSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated is False:
            return Item.objects.filter(owner__profile__isPublic = True)
        elif self.request.user.is_superuser:
            return Item.objects.all()
        else:
            return Item.objects.filter(
                Q(owner__profile__isPublic = True) |
                Q(owner__profile__share_with__user__id = self.request.user.id) |
                Q(owner__id = self.request.user.id)
            )

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user) 

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = VoleaUserDetailsSerializer
