from django import forms

from Projekat.literature.models import Literature, LiteratureNote


class LiteratureForm(forms.ModelForm):
    class Meta:
        model = Literature
        fields = ['title', 'authors', 'journal', 'year', 'volume',
                 'issue', 'pages', 'doi', 'is_public']
        widgets = {
            'authors': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'title': 'Naslov rada',
            'authors': 'Autori',
            'journal': 'Časopis',
            'year': 'Godina',
            'volume': 'Volumen',
            'issue': 'Broj',
            'pages': 'Stranice',
            'doi': 'DOI',
            'is_public': 'Javno dostupno',
        }

    def clean_doi(self):
        doi = self.cleaned_data.get('doi')
        if doi:
            if not doi.startswith('10.'):
                raise forms.ValidationError('doi mora poceti sa 10.')
        return doi

class LiteratureNoteForm(forms.ModelForm):
    class Meta:
        model = LiteratureNote
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Uneti belesku...'}),
        }
