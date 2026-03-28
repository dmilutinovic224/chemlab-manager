from django import forms
from Projekat.core.models import Compound, Property, Coment


class CompoundForm(forms.ModelForm):
    class Meta:
        model = Compound
        fields = ['name', 'iupac', 'smiles', 'cas_num', 'formula', 'mweight', 'area', 'public', 'category']
        widgets = {
            'iupac': forms.Textarea(attrs={'rows': 2}),
            'smiles': forms.TextInput(attrs={'placeholder': 'npr. CCO'}),
            'cas_num': forms.TextInput(attrs={'placeholder': 'npr. 64-17-5'}),
        }
        labels = {
            'name': 'Naziv',
            'iupac': 'iupac naziv',
            'smiles': 'smiles',
            'cas_num': 'cas broj',
            'formula': 'formula',
            'mweight': 'Molekulska masa (g/mol)',
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'field': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_mweight(self):
        mw = self.cleaned_data.get('mweight')
        if mw is not None and mw <= 0:
            raise forms.ValidationError('molekulska masa mora biti prirodan broj')
        return mw

    def clean_smiles(self):
        smiles = self.cleaned_data.get('smiles')
        if smiles:
            if ' ' in smiles:
                raise forms.ValidationError('smiles unos ne sme da ima razmak')
        return smiles

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['property_type', 'value', 'unit']

class ComentForm(forms.ModelForm):
    class Meta:
        model = Coment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Unesite komentar..'}),
        }
        labels = {
            'text': '',
        }
# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['name']
#
# class CompoundCategoryForm(forms.ModelForm):
#     class Meta:
#         model = CompoundCategory
#         fields = ['category_type']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['category'].queryset = Category.objects.all()

class SpectrumForm(forms.ModelForm):
    pass

#################################
# class ReceptForm(forms.ModelForm):
#     class Meta:
#         model = Recept
#         fields = ['naziv', 'opis', 'javno']
#         widgets = {
#             'opis': forms.Textarea(attrs={'rows': 4}),
#         }
#         labels = {
#             'naziv': 'Naziv recepta',
#             'opis': 'Opis pripreme',
#             'javno': 'Javno dostupan',
#         }
# class SastojakForm(forms.ModelForm):
#     class Meta:
#         model = Sastojak
#         fields = ['naziv', 'kolicina']
#
# class KomentarForm(forms.ModelForm):
#     class Meta:
#         model = Komentar
#         fields = ['tekst']
#         widgets = {
#             'tekst': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Unesite vaš komentar...'}),
#         }
#         labels = {
#             'tekst': '',
#         }
# class KategorijaForm(forms.ModelForm):
#     class Meta:
#         model = Kategorija
#         fields = ['naziv']
#
# class ReceptKategorijaForm(forms.ModelForm):
#     class Meta:
#         model = ReceptKategorija
#         fields = ['kategorija']
#         labels = {
#             'kategorija': 'Izaberi kategoriju',
#         }