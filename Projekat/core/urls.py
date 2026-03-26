from django.urls import path
from Projekat.core import views
#from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('compounds/', views.CompoundListView.as_view(), name='compound_list'),
    path('compounds/<int:pk>/', views.CompoundDetailView.as_view(), name='compound_detail'),
    # prijava
    # path('moji/', views.MojiReceptiView.as_view(), name='moji_recepti'),
    path('compounds/dodaj/', views.CompoundCreateView.as_view(), name='compound_create'),
    path('compounds/<int:pk>/uredi/', views.CompoundUpdateView.as_view(), name='compound_update'),
    path('compounds/<int:pk>/obrisi/', views.CompoundDeleteView.as_view(), name='compound_delete'),
    path('compounds/<int:pk>/dodaj-svojstvo/', views.PropertyCreateView.as_view(), name='property_create'),
    path('compounds/<int:pk>/dodaj-komentar/', views.ComentView.as_view(), name='comment_create'),
    path('compounds/<int:pk>/obrisi-komentar/', views.CommentDeleteView.as_view(), name='comment_delete'),
    # path('compounds/dodaj-kategoriju/', views.CategoryView.as_view(), name='category_create'),

    # path('kategorije/dodaj/', views.CategoryView.as_view(), name='category_create'),
    # path('compounds/<int:pk>/dodaj-kategoriju/', views.CompoundCategoryView.as_view(), name='compoundcategory_create'),
    # path('recept/<int:recept_pk>/dodaj-kategoriju/', views.ReceptKategorijaView.as_view(), name='recept_kategorija_create'),

]