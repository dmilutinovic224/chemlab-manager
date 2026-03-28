from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from Projekat.inventory.forms import SupplierForm, ChemicalForm, BatchForm, InventoryNoteForm
from Projekat.inventory.models import Supplier, Chemical, Batch, InventoryNote


class SupplierListView(ListView):
    model = Supplier
    template_name = 'inventory/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 4

    def get_queryset(self):
        q= Supplier.objects.all()
        search = self.request.GET.get('search')
        if search:
            q = q.filter(Q(name__icontains=search) | Q(contact__icontains=search) | Q(email__icontains=search) )
        return q

class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'inventory/supplier_detail.html'
    context_object_name = 'supplier'

class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('supplier_list')

    def form_valid(self, form):
        # form.instance.created_by = self.request.user
        return super().form_valid(form)

class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('supplier_list')

    def get_queryset(self):
        return Supplier.objects.filter(created_by=self.request.user)

    def form_valid(self, form):
        return super().form_valid(form)


class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'inventory/supplier_delete.html'
    success_url = reverse_lazy('supplier_list')

##################
class ChemicalListView(ListView):
    model = Chemical
    template_name = 'inventory/chemical_list.html'
    context_object_name = 'chemicals'
    paginate_by = 4

    def get_queryset(self):
        q= Chemical.objects.all()
        search = self.request.GET.get('search')
        if search:
            q = q.filter(Q(name__icontains=search) | Q(cas_number__icontains=search) | Q(formula__icontains=search) )
        return q

class ChemicalDetailView(DetailView):
    model = Chemical
    template_name = 'inventory/chemical_detail.html'
    context_object_name = 'chemical'

class ChemicalCreateView(LoginRequiredMixin, CreateView):
    model = Chemical
    form_class = ChemicalForm
    template_name = 'inventory/chemical_form.html'
    success_url = reverse_lazy('chemical_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ChemicalUpdateView(LoginRequiredMixin, UpdateView):
    model = Chemical
    form_class = ChemicalForm
    template_name = 'inventory/chemical_form.html'
    success_url = reverse_lazy('chemical_list')

    def get_queryset(self):
        return Chemical.objects.filter(created_by=self.request.user)

    def form_valid(self, form):
        return super().form_valid(form)

class ChemicalDeleteView(LoginRequiredMixin, DeleteView):
    model = Chemical
    template_name = 'inventory/chemical_delete.html'
    success_url = reverse_lazy('chemical_list')


##########
class BatchListView(ListView):
    model = Batch
    template_name = 'inventory/batch_list.html'
    context_object_name = 'batches'
    # paginate_by = 4

    def get_queryset(self):
        q= Batch.objects.all()
        search = self.request.GET.get('search')
        if search:
            q = q.filter(Q(batch_number__icontains=search) | Q(chemical__name__icontains=search) | Q(catalog__icontains=search))
        return q.select_related('chemical', 'supplier')

class BatchDetailView(DetailView):
    model = Batch
    template_name = 'inventory/batch_detail.html'
    context_object_name = 'batch'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inv_notes'] = self.object.inv_notes.all()
        return context

class BatchCreateView(LoginRequiredMixin, CreateView):
    model = Batch
    form_class = BatchForm
    template_name = 'inventory/batch_form.html'
    success_url = reverse_lazy('batch_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class BatchUpdateView(LoginRequiredMixin, UpdateView):
    model = Batch
    form_class = BatchForm
    template_name = 'inventory/batch_form.html'
    success_url = reverse_lazy('batch_list')

    def get_queryset(self):
        return Batch.objects.filter(created_by=self.request.user)

    def form_valid(self, form):
        return super().form_valid(form)

class BatchDeleteView(LoginRequiredMixin, DeleteView):
    model = Batch
    template_name = 'inventory/batch_delete.html'
    success_url = reverse_lazy('batch_list')

##########
class InventoryNoteCreateView(LoginRequiredMixin, CreateView):
    model = InventoryNote
    form_class = InventoryNoteForm
    template_name = 'inventory/inventorynote_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.batch = get_object_or_404(Batch, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.batch = self.batch
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('batch_detail', kwargs={'pk': self.batch.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['batch'] = self.batch
        return context

class InventoryNoteDeleteView(LoginRequiredMixin, DeleteView):
    model = InventoryNote
    template_name = 'inventory/inventorynote_delete.html'

    def get_queryset(self):
        return InventoryNote.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('batch_detail', kwargs={'pk': self.object.batch.pk})

# Create your views here.
