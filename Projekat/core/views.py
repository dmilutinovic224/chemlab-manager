# from django.contrib.auth import login
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from Projekat.core.tasks import calculatecompoundprops, generatesmiles3d
from Projekat.core.smiles import smiles3d
from django.shortcuts import render, redirect, get_object_or_404

from Projekat.core.forms import CompoundForm, PropertyForm, ComentForm
from Projekat.core.models import Compound, Property, Coment

from Projekat.literature.models import Literature
from Projekat.experiments.models import Experiment
from Projekat.inventory.models import Chemical


class CompoundListView(ListView):
    model = Compound
    template_name = 'core/compound_list.html'
    context_object_name = 'compounds'

    def get_queryset(self):
        return Compound.objects.filter(public=True).order_by('-created_by')

class CompoundDetailView(DetailView):
    model = Compound
    template_name = 'core/compound_detail.html'
    context_object_name = 'compound'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        compound = self.get_object()

        context['has_3d'] = False
        context['pdb_data'] = None
        context['smiles_error'] = None

        # if compound.smiles:
        #     result = smiles3d(compound.smiles)
        #     if result['success']:
        #         context['has_3d'] = True
        #         context['pdb_data'] = result['pdb']
        #     else:
        #         context['smiles_error'] = result['err']

        return context

class CompoundCreateView(LoginRequiredMixin,CreateView):
    model = Compound
    form_class = CompoundForm
    template_name = 'core/compound_form.html'
    success_url = reverse_lazy('compound_list')

    def form_valid(self, form):
        print(f"Korisnik: {self.request.user}")
        print(f"ID korisnika: {self.request.user.id}")   #debag
        print(f"Prijavljen: {self.request.user.is_authenticated}")
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        if form.instance.smiles:
            calculatecompoundprops.delay(self.object.id)
            generatesmiles3d.delay(self.object.id)
        return response


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def handle_no_permission(self):
        return redirect('login')

class CompoundUpdateView(LoginRequiredMixin, UpdateView):
    model = Compound
    form_class = CompoundForm
    template_name = 'core/compound_form.html'
    success_url = reverse_lazy('compound_list')

    def get_queryset(self):
        return Compound.objects.filter(created_by=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        if 'smiles' in form.changed_data and form.instance.smiles:
            calculatecompoundprops.delay(self.object.id)
            generatesmiles3d.delay(self.object.id)
        return response

class CompoundDeleteView(LoginRequiredMixin, DeleteView):
    model = Compound
    template_name = 'core/compound_delete.html'
    success_url = reverse_lazy('compound_list')

    def get_queryset(self):
        return Compound.objects.filter(created_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        # messages.success(request, 'Recept uspešno obrisan.')
        return super().delete(request, *args, **kwargs)

##################
class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'core/property_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.compound = get_object_or_404(Compound, pk=kwargs['pk'])
        if self.compound.created_by != request.user:
            # messages.error(request, 'Nemate pravo dodavati sastojke u tuđi recept.')
            return redirect('compound_detail', pk=self.compound.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        print("ok")
        form.instance.compound = self.compound
        form.instance.added_by = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print("ne valja!")
        print(form.errors)
        messages.error(self.request, 'ERR.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('compound_detail', kwargs={'pk': self.object.compound.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['compound'] = self.compound
        return context

##################
class ComentView(LoginRequiredMixin, CreateView):
    model = Coment
    form_class = ComentForm
    template_name = 'core/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.compound = get_object_or_404(Compound, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.compound = self.compound
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['compound'] = self.compound
        return context

    def get_success_url(self):
        return reverse_lazy('compound_detail', kwargs={'pk': self.object.compound.pk})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Coment
    template_name = 'core/comment_delete.html'

    def get_queryset(self):
        return Coment.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('compound_detail', kwargs={'pk': self.object.compound.pk})

##################
# class CategoryView(LoginRequiredMixin, CreateView):
#     model = Category
#     form_class = CategoryForm
#     template_name = 'core/category_form.html'
#     success_url = reverse_lazy('compound_list')
#
#     def form_valid(self, form):
#         return super().form_valid(form)



# class CompoundCategoryView(LoginRequiredMixin, CreateView):
#     model = CompoundCategory
#     form_class = CompoundCategoryForm
#     template_name = 'core/compoundcategory_form.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         self.compound = get_object_or_404(Compound, pk=kwargs['pk'])
#         return super().dispatch(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         form.instance.compound = self.compound
#         return super().form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['compound'] = self.compound
#         return context
#
#     def get_success_url(self):
#         return reverse_lazy('compound_detail', kwargs={'pk': self.compound.pk})

################
def home(request): #fja za  homepage
    context = {
        'numcompounds': Compound.objects.filter(public=True).count(),
        'numliterature': Literature.objects.filter(is_public=True).count(),
        'numexperiments': Experiment.objects.filter(is_public=True).count(),
        'numchemicals': Chemical.objects.count(),
    }
    return render(request, 'core/home.html', context)

##########################################
class SpectrumCreateView(LoginRequiredMixin, CreateView):
    pass

class SpectrumDeleteView(LoginRequiredMixin, DeleteView):
    pass
#############################################################################################################
# Create your views here.
# class ReceptListView(ListView):
#     model = Recept
#     template_name = 'recept_list.html'
#     context_object_name = 'recepti'
#
#     def get_queryset(self):
#         return Recept.objects.filter(javno=True).order_by('-created')
#
# class ReceptDetailView(DetailView):
#     model = Recept
#     template_name = 'recept_detail.html'
#     context_object_name = 'recept'
#
# class ReceptCreateView(LoginRequiredMixin,CreateView):
#     model = Recept
#     form_class = ReceptForm
#     template_name = 'recept_form.html'
#     success_url = reverse_lazy('recept_list')
#
#     def form_valid(self, form):
#         print(f"Korisnik: {self.request.user}")
#         print(f"ID korisnika: {self.request.user.id}")
#         print(f"Prijavljen: {self.request.user.is_authenticated}")
#         form.instance.autor = self.request.user
#         return super().form_valid(form)
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         return kwargs
#
#     def handle_no_permission(self):
#         return redirect('login')
#
# class ReceptUpdateView(LoginRequiredMixin, UpdateView):
#     model = Recept
#     form_class = ReceptForm
#     template_name = 'recept_form.html'
#     success_url = reverse_lazy('recept_list')
#
#     def get_queryset(self):
#         return Recept.objects.filter(autor=self.request.user)
#
# class ReceptDeleteView(LoginRequiredMixin, DeleteView):
#     model = Recept
#     template_name = 'recept_delete_conf.html'
#     success_url = reverse_lazy('recept_list')
#
#     def get_queryset(self):
#         return Recept.objects.filter(autor=self.request.user)
#
#     def delete(self, request, *args, **kwargs):
#         messages.success(request, 'Recept uspešno obrisan.')
#         return super().delete(request, *args, **kwargs)
#
# ##################
# class SastojakCreateView(LoginRequiredMixin, CreateView):
#     model = Sastojak
#     form_class = SastojakForm
#     template_name = 'sastojak_form.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         self.recept = get_object_or_404(Recept, pk=kwargs['recept_pk'])
#         if self.recept.autor != request.user:
#             messages.error(request, 'Nemate pravo dodavati sastojke u tuđi recept.')
#             return redirect('recept_detail', pk=self.recept.pk)
#         return super().dispatch(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         form.instance.recept = self.recept
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('recept_detail', kwargs={'pk': self.object.recept.pk})
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['recept'] = self.recept
#         return context
#
# ##################
# class KomentarView(LoginRequiredMixin, CreateView):
#     model = Komentar
#     form_class = KomentarForm
#     template_name = 'komentar_form.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         self.recept = get_object_or_404(Recept, pk=kwargs['recept_pk'])
#         return super().dispatch(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         form.instance.recept = self.recept
#         form.instance.autor = self.request.user
#         return super().form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['recept'] = self.recept
#         return context
#
#     def get_success_url(self):
#         return reverse_lazy('recept_detail', kwargs={'pk': self.object.recept.pk})
#
# ##################
# class KategorijaView(LoginRequiredMixin, CreateView):
#     model = Kategorija
#     form_class = KategorijaForm
#     template_name = 'kategorija_form.html'
#     success_url = reverse_lazy('recept_list')
#
#     def form_valid(self, form):
#         return super().form_valid(form)
#
# ################
# class ReceptKategorijaView(LoginRequiredMixin, CreateView):
#     model = ReceptKategorija
#     form_class = ReceptKategorijaForm
#     template_name = 'recept_kategorija_form.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         self.recept = get_object_or_404(Recept, pk=kwargs['recept_pk'])
#         if self.recept.autor != request.user:
#             messages.error(request, 'Samo autor može dodavati kategorije.')
#             return redirect('recept_detail', pk=self.recept.pk)
#         return super().dispatch(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         form.instance.recept = self.recept
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('recept_detail', kwargs={'pk': self.recept.pk})
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['recept'] = self.recept
#         return context