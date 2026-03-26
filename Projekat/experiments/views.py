from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db import models
from Projekat.experiments.forms import ExperimentForm, ExperimentNoteForm
from Projekat.experiments.models import Experiment, ExperimentNote


class ExperimentListView(ListView):
    model = Experiment
    template_name = 'experiments/experiment_list.html'
    context_object_name = 'experiments'
    paginate_by = 5

    def get_queryset(self):
        return Experiment.objects.filter(is_public=True)

class ExperimentDetailView(DetailView):
    model = Experiment
    template_name = 'experiments/experiment_detail.html'
    context_object_name = 'experiment'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Experiment.objects.filter(
                models.Q( is_public=True) |
                models.Q(created_by=self.request.user)
            )
        return Experiment.objects.filter( is_public=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = self.object.notes.all()
        context['experiment'] = self.object
        return context

class ExperimentCreateView(LoginRequiredMixin, CreateView):
    model = Experiment
    form_class = ExperimentForm
    template_name = 'experiments/experiment_form.html'
    success_url = reverse_lazy('experiment_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ExperimentUpdateView(LoginRequiredMixin, UpdateView):
    model = Experiment
    form_class = ExperimentForm
    template_name = 'experiments/experiment_form.html'
    success_url = reverse_lazy('experiment_list')

    def get_queryset(self):
        return Experiment.objects.filter(created_by=self.request.user)

    def form_valid(self, form):
        return super().form_valid(form)

class ExperimentDeleteView(LoginRequiredMixin, DeleteView):
    model = Experiment
    template_name = 'experiments/experiment_delete.html'
    success_url = reverse_lazy('experiment_list')

    def get_queryset(self):
        return Experiment.objects.filter(created_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

##################
class ExperimentNoteCreateView(LoginRequiredMixin, CreateView):
    model = ExperimentNote
    form_class = ExperimentNoteForm
    template_name = 'experiments/exp_note_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.experiment = get_object_or_404(Experiment, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.experiment = self.experiment
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiment'] = self.experiment
        return context

    def get_success_url(self):
        return reverse_lazy('experiment_detail', kwargs={'pk': self.object.experiment.pk})

class ExperimentNoteDeleteView(LoginRequiredMixin, DeleteView):
    model = ExperimentNote
    template_name = 'experiments/exp_delete_form.html'

    def get_queryset(self):
        return ExperimentNote.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('experiment_detail', kwargs={'pk': self.object.experiment.pk})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

# Create your views here.
