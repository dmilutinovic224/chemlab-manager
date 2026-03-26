from django.contrib import admin
from .models import Supplier, Chemical, Batch, InventoryNote

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact', 'email', 'phone', 'website']
    search_fields = ['name', 'contact', 'email']

@admin.register(Chemical)
class ChemicalAdmin(admin.ModelAdmin):
    list_display = ['name', 'cas_number', 'formula', 'molecular_weight', 'compound', 'un_number']
    search_fields = ['name', 'cas_number', 'formula']
    list_filter = ['formula']

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['chemical', 'batch_number', 'supplier', 'quantity', 'unit', 'expiry_date', 'location']
    list_filter = ['expiry_date', 'received_date']
    search_fields = ['batch_number', 'chemical__name', 'catalog_number']
    raw_id_fields = ['chemical', 'supplier']

@admin.register(InventoryNote)
class InventoryNoteAdmin(admin.ModelAdmin):
    list_display = ['batch', 'user', 'note', 'created_at']
    list_filter = ['created_at']
    search_fields = ['note', 'user__username', 'batch__batch_number']
