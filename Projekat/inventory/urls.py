from django.urls import path
from Projekat.inventory import views

urlpatterns = [
    ############
    path('supplier/', views.SupplierListView.as_view(), name='supplier_list'),
    path('supplier/<int:pk>/', views.SupplierDetailView.as_view(), name='supplier_detail'),
    path('supplier/dodaj/', views.SupplierCreateView.as_view(), name='supplier_create'),
    path('supplier/<int:pk>/uredi/', views.SupplierUpdateView.as_view(), name='supplier_update'),
    path('supplier/<int:pk>/obrisi/', views.SupplierDeleteView.as_view(), name='supplier_delete'),
    ############
    path('chemical/', views.ChemicalListView.as_view(), name='chemical_list'),
    path('chemical/<int:pk>/', views.ChemicalDetailView.as_view(), name='chemical_detail'),
    path('chemical/dodaj/', views.ChemicalCreateView.as_view(), name='chemical_create'),
    path('chemical/<int:pk>/uredi/', views.ChemicalUpdateView.as_view(), name='chemical_update'),
    path('chemical/<int:pk>/obrisi/', views.ChemicalDeleteView.as_view(), name='chemical_delete'),
    ############
    path('batch/', views.BatchListView.as_view(), name='batch_list'),
    path('batch/<int:pk>/', views.BatchDetailView.as_view(), name='batch_detail'),
    path('batch/dodaj/', views.BatchCreateView.as_view(), name='batch_create'),
    path('batch/<int:pk>/uredi/', views.BatchUpdateView.as_view(), name='batch_update'),
    path('batch/<int:pk>/obrisi/', views.BatchDeleteView.as_view(), name='batch_delete'),

    path('batch/<int:pk>/dodaj-note/', views.InventoryNoteCreateView.as_view(), name='inventory_note_create'),
    path('note/<int:pk>/obrisi-note/', views.InventoryNoteDeleteView.as_view(), name='inventory_note_delete'),
]