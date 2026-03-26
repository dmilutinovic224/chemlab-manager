from django.urls import path
from Projekat.experiments import views

urlpatterns = [
    path('', views.ExperimentListView.as_view(), name='experiment_list'),
    path('<int:pk>/', views.ExperimentDetailView.as_view(), name='experiment_detail'),
    path('dodaj/', views.ExperimentCreateView.as_view(), name='experiment_create'),
    path('<int:pk>/uredi/', views.ExperimentUpdateView.as_view(), name='experiment_update'),
    path('<int:pk>/obrisi/', views.ExperimentDeleteView.as_view(), name='experiment_delete'),
    path('<int:pk>/dodaj-exp-notes/', views.ExperimentNoteCreateView.as_view(), name='experiment_note_create'),
    path('exp-notes/<int:pk>/obrisi/', views.ExperimentNoteDeleteView.as_view(), name='experiment_note_delete'),
]
