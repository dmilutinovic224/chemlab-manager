from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class Compound(models.Model):
    AREA = [
        #oblasti....(prosiriti)
        ('inorg', 'neorganska'),
        ('org', 'organska'),
        ('an', 'analitička'),
        ('phus', 'fizicka'),
        ('bch', 'biohemija'),
    ]
    CATEGS = [
        ('OXIDES', 'Oksidi'),
        ('INORG_ACIDS', 'Kiseline (Neorganske)'),
        ('BASES', 'Baze / Hidroksidi'),
        ('SALTS', 'Soli'),
        ('METALS', 'Metali i Legure'),
        ('NONMETALS', 'Nemetali'),
        ('COMPLEXES', 'Koordinaciona jedinjenja'),
        ('HYDROCARBONS', 'Ugljovodonici'),
        ('AROMATICS', 'Aromatična jedinjenja'),
        ('ALCOHOLS', 'Alkoholi i Fenoli'),
        ('CARBOXYLIC', 'Karboksilne kiseline'),
        ('CARBONYLS', 'Aldehidi i Ketoni'),
        ('ESTERS', 'Estri i Etri'),
        ('AMINES', 'Amini i Amidi'),
        ('ORGANOMETALLIC', 'Organometalna jedinjenja'),
        ('POLYMERS', 'Sintetički polimeri'),
        ('PROTEINS', 'Proteini / Peptidi'),
        ('CARBOHYDRATES', 'Ugljeni hidrati'),
        ('LIPIDS', 'Lipidi'),
        ('NUCLEIC', 'Nukleinske kiseline'),
        ('SOLVENTS', 'Rastvarači'),
        ('CATALYSTS', 'Katalizatori'),
        ('MIXTURES', 'Smeše / Formulacije'),
        ('REAGENTS', 'Reagensi'),
    ]
    name = models.CharField(max_length=50)
    iupac = models.CharField(max_length=50, blank=True)
    area = models.CharField(max_length=50, choices=AREA)
    smiles = models.CharField(max_length=50, blank=True)
    inchi = models.CharField(max_length=50, blank=True)
    formula = models.CharField(max_length=50)
    mweight = models.FloatField(null=True, blank=True)
    cas_num = models.CharField(max_length=50, blank=True)
    public = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compounds') #NE MENJAJ!!!!!!
    created = models.DateTimeField(auto_now_add=True)
    uploaded = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=50, choices=CATEGS, blank=True,null=True,)
    ################polja ispod za async
    logp = models.FloatField(null=True, blank=True)
    surface = models.FloatField(null=True, blank=True)
    h_donors = models.IntegerField(null=True, blank=True)
    h_acc = models.IntegerField(null=True, blank=True)
    pdb = models.FileField(upload_to='pdb/', null=True, blank=True)
    structure = models.BooleanField(default=False)
    calcproperties = models.BooleanField(default=False)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/Compound/{self.id}/'

class Property(models.Model):
    TYPES = [
        #neke osobine(dodati refrakciju, tpl provodlj, viskoznost, kristalna str, gr simetrije, dipol, topl kap,...)
        ('tt', 'tacka topljenja (°C)'),
        ('tk', 'tacka kljucanja (°C)'),
        ('r', 'rastvorljivost (g/L)'),
        ('gst', 'gustina (g/cm3)'),
        ('logp', 'logP'),
        ('pk', 'pKa'),
    ]
    compound = models.ForeignKey(Compound, on_delete=models.CASCADE, related_name='properties')#NE MENAJ!!!!!!
    property_type = models.CharField(max_length=50, choices=TYPES)

    value = models.FloatField()
    unit = models.CharField(max_length=50, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    # kolicina = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.compound.name} - {self.property_type}'

# class Category(models.Model):
#     name = models.CharField(max_length=50)
#
#
#     def __str__(self):
#         return self.name

# class CompoundCategory(models.Model):
#
#     compound = models.ForeignKey(Compound, on_delete=models.CASCADE, related_name='categores')
#     # category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     category_type = models.CharField(max_length=50, choices=CATEGS, unique=True)
#
#     class Meta:
#         unique_together = ['compound', 'category']
#
#     def __str__(self):
#         return f'{self.compound.name} - {self.category.name}'

class Coment(models.Model):
    compound = models.ForeignKey(Compound, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Komentar od {self.autor.username}'

class Spectrum(models.Model):
    TYPES = [
        ('ir','ir'),
        ('nmr', 'nmr'),
        ('ms', 'ms'),
    ]
    compound = models.ForeignKey(Compound, on_delete=models.CASCADE, related_name='spectra')  #
    spectrumtype = models.CharField(max_length=50, choices=TYPES)
    info = models.TextField()
    image = models.ImageField(upload_to='spectra/', blank=True, null=True) #slika
    # image = models.FileField(upload_to='spectra/', blank=True, null=True) #pdf
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.compound.name} - {self.spectrumtype}'

# Create your models here.







# class Recept(models.Model):
#     naziv = models.CharField(max_length=200)
#     opis = models.TextField()
#     autor = models.ForeignKey(User, on_delete=models.CASCADE)
#     javno = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.naziv
#
#     def get_absolute_url(self):
#         return f'/recept/{self.id}/'
#
# class Sastojak(models.Model):
#     recept = models.ForeignKey(Recept, on_delete=models.CASCADE, related_name='sastojci')
#     naziv = models.CharField(max_length=100)
#     kolicina = models.CharField(max_length=50)
#
#     def __str__(self):
#         return f'{self.naziv} - {self.kolicina}'
#
# class Kategorija(models.Model):
#     naziv = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.naziv
#
# class ReceptKategorija(models.Model):
#     recept = models.ForeignKey(Recept, on_delete=models.CASCADE)
#     kategorija = models.ForeignKey(Kategorija, on_delete=models.CASCADE)
#
#     class Meta:
#         unique_together = ['recept', 'kategorija']
#
# class Komentar(models.Model):
#     recept = models.ForeignKey(Recept, on_delete=models.CASCADE, related_name='komentari')
#     autor = models.ForeignKey(User, on_delete=models.CASCADE)
#     tekst = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'Komentar od {self.autor.username}'