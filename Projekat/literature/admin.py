from django.contrib import admin
from .models import Literature, LiteratureNote

@admin.register(Literature)
class LiteratureAdmin(admin.ModelAdmin):
    list_display = ['title', 'authors', 'journal', 'year', 'uploaded_by', 'status']
    list_filter = ['status', 'is_public', 'year']
    search_fields = ['title', 'authors', 'doi']

@admin.register(LiteratureNote)
class LiteratureNoteAdmin(admin.ModelAdmin):
    list_display = ['literature', 'user', 'created_at']
    list_filter = ['created_at']

# Register your models here.
