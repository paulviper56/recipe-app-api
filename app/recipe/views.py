from django.shortcuts import render
from .serializers import RecipeSerializer, RecipeDetailSerializer
from rest_framework import generics, authentication, permissions,viewsets
from core.models import Recipe

# Create your views here.
class RecipeViewAPI(viewsets.ModelViewSet):
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):

        if self.action == 'list':
            return RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):

        return serializer.save(user= self.request.user)