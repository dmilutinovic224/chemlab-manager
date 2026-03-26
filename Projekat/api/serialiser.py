from django.contrib.auth import get_user_model
from rest_framework import serializers

from Projekat.core.models import Compound, Property,  Coment
from Projekat.experiments.models import Experiment
from Projekat.inventory.models import Supplier, Chemical, Batch
from Projekat.literature.models import Literature

User = get_user_model()




# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name',]

class ComentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Coment
        fields = ['id', 'compound', 'user', 'text', 'created','username']
        read_only = ['id', 'created', 'user',]

class PropertySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='added_by.username', read_only=True)
    display = serializers.CharField(source='get_property_type_display', read_only=True)
    class Meta:
        model = Property
        fields = ['id', 'property_type', 'value', 'unit', 'added_by',  'created','username','display']
        read_only = ['id', 'created', ]

class CompoundSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='created_by.username', read_only=True)
    class Meta:
        model = Compound
        fields = ['id', 'name', 'iupac',  'cas_num', 'formula',  'area', 'public', 'created_by', 'created','username', 'category']
        read_only = ['id', 'created',]



class CompoundDetailSerializer(CompoundSerializer):
    properties = PropertySerializer(many=True, read_only=True)
    # categories = CategorySerializer(many=True, read_only=True)
    categories =  serializers.SerializerMethodField()
    comments=ComentSerializer(many=True, read_only=True)
    class Meta:
        fields = ['id', 'name', 'iupac',  'cas_num', 'formula',  'area', 'public', 'created_by', 'created', 'properties', 'category', 'category_display', 'comments',]
    # def get_categories(self,obj):
    #     categories =[]
    #     for cc in obj.compoundcategory_set.all():
    #         categories.append(cc.category)
    #     return CategorySerializer(categories, many=True).data
##########################################################

class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = ['id','title', 'description', 'experiment_type', 'status', 'is_public']
        read_only = ['id', 'created_at', ]

#########################################################

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact', 'email', 'phone', 'website']

class ChemicalSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='created_by.username', read_only=True)
    compoundname = serializers.CharField(source='compound.name', read_only=True)
    class Meta:
        model = Chemical
        fields = ['id','name', 'cas_number', 'formula', 'molecular_weight', 'compound', 'un_number', 'hazard_symbol','username','compoundname']

class BatchSerializer(serializers.ModelSerializer):
    chem_name = serializers.CharField(source='chemical.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    username = serializers.CharField(source='created_by.username', read_only=True)
    expired = serializers.BooleanField(read_only=True)
    class Meta:
        model = Batch
        fields = ['chemical', 'supplier', 'batch_number', 'catalog_number', 'quantity', 'unit', 'purity', 'received_date', 'expiry_date', 'location', 'msds', 'coa', 'notes', 'chem_name', 'supplier_name', 'username',]
        read_only = ['id', 'created_by']

################################################################ Literature

class LiteratureSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='uploaded_by.username', read_only=True)
    class Meta:
        model = Literature
        fields = ['id','title', 'authors', 'journal', 'year', 'volume','issue', 'pages', 'doi', 'is_public','uploaded_by','username']
        read_only = ['id', 'created_at', ]

#!################################################

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'institution']
