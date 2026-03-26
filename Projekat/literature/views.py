from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db import models
from Projekat.literature.forms import LiteratureForm, LiteratureNoteForm
from Projekat.literature.models import Literature, LiteratureNote


class LiteratureListView(ListView):
    model = Literature
    template_name = 'literature/literature_list.html'
    context_object_name = 'literature'
    paginate_by = 8

    def get_queryset(self):
        return Literature.objects.filter(is_public=True)

class LiteratureDetailView(DetailView):
    model = Literature
    template_name = 'literature/literature_detail.html'
    context_object_name = 'paper'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Literature.objects.filter(
                models.Q( is_public=True) |
                models.Q(uploaded_by=self.request.user)
            )
        return Literature.objects.filter( is_public=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = self.object.notes.all()
        context['paper'] = self.object
        return context

class LiteratureCreateView(LoginRequiredMixin, CreateView):
    model = Literature
    form_class = LiteratureForm
    template_name = 'literature/literature_form.html'
    success_url = reverse_lazy('literature_list')

    def form_valid(self, form):
        print("createforma")
        form.instance.uploaded_by = self.request.user
        form.instance.status = 'DRAFT'
        return super().form_valid(form)

class LiteratureUpdate(LoginRequiredMixin, UpdateView):
    model = Literature
    form_class = LiteratureForm
    template_name = 'literature/literature_form.html'
    success_url = reverse_lazy('literature_list')

    def form_valid(self, form):
        return super().form_valid(form)

    def get_queryset(self):
        return Literature.objects.filter(uploaded_by=self.request.user)

class LiteratureDeleteView(LoginRequiredMixin, DeleteView):
    model = Literature
    template_name = 'literature/literature_delete.html'
    success_url = reverse_lazy('literature_list')

    def get_queryset(self):
        return Literature.objects.filter(uploaded_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class LiteratureNoteCreateView(LoginRequiredMixin, CreateView):
    model = LiteratureNote
    form_class = LiteratureNoteForm
    template_name = 'literature/note_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.literature = get_object_or_404(Literature, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.literature = self.literature
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['literature'] = self.literature
        return context

    def get_success_url(self):
        return reverse_lazy('literature_detail', kwargs={'pk': self.object.literature.pk})




class LiteratureNoteDeleteView(LoginRequiredMixin, DeleteView):
    model = LiteratureNote
    template_name = 'literature/note_delete.html'

    def get_queryset(self):
        return LiteratureNote.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('literature_detail', kwargs={'pk': self.object.literature.pk})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
# Create your views here.
