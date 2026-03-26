from django.contrib.auth import get_user_model
from django.db import models

from Projekat.core.models import Compound

User = get_user_model()

class Experiment(models.Model):
    TYPES = [
        ('SYNTH', 'Sinteza'),
        ('CHAR', 'Karakterizacija'),
        ('COMP', 'Racunarski'),
        ('KINET', 'Kinetika'),
    ]
    STATUS = [
        ('PLAN', 'Planiran'),
        ('PROG', 'U toku'),
        ('DONE', 'Zavrsen'),
        ('FAIL', 'Neuspesan'),
    ]
    title = models.CharField(max_length=50)
    description = models.TextField()
    experiment_type = models.CharField(max_length=50, choices=TYPES)
    status = models.CharField(max_length=50, choices=STATUS)
    compounds = models.ManyToManyField(Compound, related_name='experiments',blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/experiments/{self.id}/'

class ExperimentNote(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note =models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Noted by: {self.user.username}"

# Create your models here.
