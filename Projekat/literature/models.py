from django.contrib.auth import get_user_model
from django.db import models

from Projekat.core.models import Compound

User = get_user_model()

class Literature(models.Model):
    title = models.CharField(max_length=50)
    authors = models.TextField()
    journal = models.CharField(max_length=50)
    year = models.IntegerField()
    volume = models.CharField(max_length=50, blank=True)
    issue = models.CharField(max_length=50, blank=True)
    pages = models.CharField(max_length=50, blank=True)
    doi = models.CharField(max_length=50, unique=True, blank=True, null=True)
    compounds = models.ManyToManyField(Compound, related_name='literature', blank=True)
    pdf = models.FileField(upload_to='literature/', blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_literature')
    STATUS_CHOICES = [
        ('DRAFT', 'Skica'),
        ('PUBLISHED', 'Objavljeno'),
        ('ARCHIVED', 'Arhivirano'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title[:25]}..."

    def get_absolute_url(self):
        return f'/literature/{self.id}/'

class LiteratureNote(models.Model):
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Noted by: {self.user.username}"

# Create your models here.
