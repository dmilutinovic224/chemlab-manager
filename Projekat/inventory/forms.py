from django import forms

from Projekat.inventory.models import Supplier, Chemical, Batch, InventoryNote


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact', 'email', 'phone', 'website']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }
class ChemicalForm(forms.ModelForm):
    class Meta:
        model = Chemical
        fields = ['name', 'cas_number', 'formula', 'molecular_weight', 'compound', 'un_number', 'hazard_symbol']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'cas_number': forms.TextInput(attrs={'class': 'form-control'}),
            'formula': forms.TextInput(attrs={'class': 'form-control'}),
            'molecular_weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'compound': forms.Select(attrs={'class': 'form-select'}),
            'un_number': forms.TextInput(attrs={'class': 'form-control'}),
            'hazard_symbols': forms.TextInput(attrs={'class': 'form-control'}),
        }
class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['chemical', 'supplier', 'batch_number', 'catalog_number', 'quantity', 'unit', 'purity', 'received_date', 'expiry_date', 'location', 'msds', 'coa', 'notes']
        widgets = {
            'chemical': forms.Select(attrs={'class': 'form-select'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control'}),
            'catalog_number': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'purity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'received_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'msds': forms.FileInput(attrs={'class': 'form-control'}),
            'coa': forms.FileInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
class InventoryNoteForm(forms.ModelForm):
    class Meta:
        model = InventoryNote
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }