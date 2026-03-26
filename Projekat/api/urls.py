from django.urls import path
from Projekat.api import views

urlpatterns = [
    path('compounds/', views.CompoundListView.as_view(), name='compound-list'),
    # path('compounds/<int:pk>/', views.CompoundDetailView.as_view(), name='compound-detail'),
    path('literature/', views.LiteratureListView.as_view(), name='literature-list'),
    path('experiments/', views.ExperimentListView.as_view(), name='experiment-list'),
    path('chemicals/', views.ChemicalListView.as_view(), name='chemical-list'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
]