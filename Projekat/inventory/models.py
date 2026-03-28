from django.contrib.auth import get_user_model
from django.db import models

from Projekat.core.models import Compound

User = get_user_model()

class Supplier(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class Chemical(models.Model):
    GHS = [
        ('GHS1', 'Eksplozivno'),
        ('GHS2', 'Zapaljivo'),
        ('GHS3', 'Oksidativno'),
        ('GHS4', 'Gas pod pritiskom'),
        ('GHS5', 'Koroyivno'),
        ('GHS6', 'Toksicno'),
        ('GHS7', 'Stetno'),
        ('GHS8', 'Opasno po zdravlje'),
        ('GHS9', 'Opasno po ziv. sredinu'),
    ]
    name = models.CharField(max_length=50)
    cas_number = models.CharField(max_length=50, blank=True)
    formula = models.CharField(max_length=50, blank=True)
    molecular_weight = models.FloatField(blank=True, null=True)
    compound = models.ForeignKey(Compound, on_delete=models.SET_NULL, blank=True, null=True, related_name='inventory_chemicals')
    un_number = models.CharField(max_length=50, blank=True)
    hazard_symbol = models.CharField(max_length=50, choices=GHS, blank=True)

    def __str__(self):
        return self.name

class Batch(models.Model):
    UNITS = [
        ('mg', 'miligram'),
        ('g', 'gram'),
        ('kg', 'kilogram'),
        ('mL', 'mililitar'),
        ('L', 'litar'),
        ('mmol', 'milimol'),
        ('mol', 'mol'),
    ]
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    chemical = models.ForeignKey(Chemical, on_delete=models.CASCADE, related_name='batches')
    batch_number = models.CharField(max_length=50)
    catalog_number = models.CharField(max_length=50, blank=True)
    unit = models.CharField(max_length=50, choices=UNITS)
    quantity = models.FloatField()
    purity = models.FloatField(null=True, blank=True)
    received_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=50, blank=True)
    msds = models.FileField(upload_to='inventory/msds/', null=True, blank=True)
    coa = models.FileField(upload_to='inventory/coa/', null=True, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.chemical.name} - {self.batch_number}"

class InventoryNote(models.Model):
    note = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='inv_notes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

# Create your models here.
