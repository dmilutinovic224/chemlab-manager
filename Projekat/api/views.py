from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, permissions
from django.db import models
from Projekat.api.serialiser import CustomUserSerializer, CompoundSerializer, LiteratureSerializer, ExperimentSerializer, ChemicalSerializer
from Projekat.core.models import Compound
from Projekat.experiments.models import Experiment
from Projekat.inventory.models import Chemical
from Projekat.literature.models import Literature

User = get_user_model()

class CompoundListView(generics.ListCreateAPIView):
    serializer_class = CompoundSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Compound.objects.filter(
                models.Q(public=True) |
                models.Q(created_by=self.request.user)
            )
        return Compound.objects.filter(public=True)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class CompoundDetailView(generics.RetrieveUpdateDestroyAPIView):
    pass

##############################################
class LiteratureListView(generics.ListCreateAPIView):
    serializer_class = LiteratureSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Literature.objects.filter(
                models.Q(is_public=True) |
                models.Q(uploaded_by=self.request.user)
            )
        return Literature.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

##############################################
class ExperimentListView(generics.ListCreateAPIView):
    serializer_class = ExperimentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Experiment.objects.filter(
                models.Q(is_public=True) |
                models.Q(created_by=self.request.user)
            )
        return Experiment.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

##############################################
class ChemicalListView(generics.ListCreateAPIView):
    serializer_class = ChemicalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Chemical.objects.all()
        return Chemical.objects.none()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

###########################################
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]






















# Create your views here.
