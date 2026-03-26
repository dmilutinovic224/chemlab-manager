from django.contrib import admin

from Projekat.core.models import Compound, Property,  Coment


@admin.register(Compound)
class CompoundAdmin(admin.ModelAdmin):
    list_display = ['name', 'iupac', 'smiles', 'cas_num', 'formula', 'mweight', 'area', 'public', 'category']
    list_filter = ['public']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['property_type', 'value', 'unit']

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', ]
#
# @admin.register(CompoundCategory)
# class CompoundCategoryAdmin(admin.ModelAdmin):
#     list_display = ['compound', 'category']



admin.site.register(Coment)
# Register your models here.
