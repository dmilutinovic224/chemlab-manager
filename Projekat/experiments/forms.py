from django import forms

from Projekat.experiments.models import Experiment, ExperimentNote


class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['title', 'description', 'experiment_type', 'status', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Unesite naziv eksperimenta'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Opišite eksperiment...'
            }),
            'experiment_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

        labels = {
            'title': 'Naziv eksperimenta',
            'description': 'Opis',
            'experiment_type': 'Tip eksperimenta',
            'status': 'Status',
            'is_public': 'Javno dostupno',
        }

        help_texts = {
            'title': 'Unesite jasan i opisni naziv',
            'experiment_type': 'Odaberite odgovarajući tip eksperimenta',
            'status': 'Trenutni status eksperimenta',
            'is_public': 'Označite ako želite da eksperiment bude vidljiv svima',
        }

        error_messages = {
            'title': {
                'required': 'Naziv je obavezan.',
                'max_length': 'Naziv je predug.',
            },
        }

class ExperimentNoteForm(forms.ModelForm):
    class Meta:
        model = ExperimentNote
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Unesite bilješku...'
            }),
        }

        labels = {
            'note': 'Bilješka',
        }

        help_texts = {
            'note': 'Dodajte bilješku o eksperimentu',
        }


