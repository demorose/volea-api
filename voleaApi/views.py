from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets
from .models import List, Item, Profile
from .serializers import ListSerializer, ItemSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly


class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated is False:
            return List.objects.filter(isPublic = True)
        elif self.request.user.is_superuser:
            return List.objects.all()
        else:
            return List.objects.filter(
                Q(isPublic = True) |
                Q(sharedWith__id = self.request.user.id) |
                Q(owner__id = self.request.user.id)
            ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user) 

        
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    filterset_fields = ['name', 'list_id']
    serializer_class = ItemSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated is False:
            return Item.objects.filter(list__isPublic = True)
        elif self.request.user.is_superuser:
            return Item.objects.all()
        else:
            return Item.objects.filter(
                Q(list__isPublic = True) |
                Q(list__sharedWith__id = self.request.user.id) |
                Q(owner__id = self.request.user.id)
            )

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user) 
        

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    filterset_fields = ['id', 'username', 'first_name', 'last_name']
    serializer_class = UserSerializer