from django.urls import path

from Projekat.core.urls import urlpatterns
from Projekat.literature import views

urlpatterns = [
    path('', views.LiteratureListView.as_view(), name='literature_list'),
    path('<int:pk>/', views.LiteratureDetailView.as_view(), name='literature_detail'),
    path('dodaj/', views.LiteratureCreateView.as_view(), name='literature_create'),
    path('<int:pk>/uredi/', views.LiteratureUpdate.as_view(), name='literature_update'),
    path('<int:pk>/obrisi/', views.LiteratureDeleteView.as_view(), name='literature_delete'),
    path('<int:pk>/dodaj-note/', views.LiteratureNoteCreateView.as_view(), name='literature_note_create'),
    path('note/<int:pk>/obrisi/', views.LiteratureNoteDeleteView.as_view(), name='literature_note_delete'),
]