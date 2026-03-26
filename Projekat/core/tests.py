from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from Projekat.core.forms import CompoundForm ,PropertyForm
from Projekat.core.models import Compound, Property, Category, Coment

User = get_user_model()

#####################MODELI#########################################
class CompoundTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username= 'username',
            password= 'password123'
        )

        self.compound = Compound.objects.create(
            name= 'Voda',
            area= 'inorg',
            formula= 'H2O',
            mweight= 18.02,
            cas_num= '64-17-5',
            created_by= self.user,
            public=True
        )

    def test_compound(self):
        self.assertEqual(self.compound.name, 'Voda')
        self.assertEqual(self.compound.area, 'inorg')
        self.assertEqual(self.compound.formula, 'H2O')
        self.assertEqual((self.compound.mweight), 18.02)
        self.assertEqual(self.compound.cas_num, '64-17-5')

    def test_namestr(self):
        self.assertEqual(str(self.compound.name), 'Voda')

    def test_MW(self):
        self.assertEqual(float(self.compound.mweight), 18.02)

    def test_MWnegative(self):
        compound = Compound(
            mweight= -18.02
        )
        with self.assertRaises(Exception):
            compound.full_clean()

    def test_createdby(self):
        self.assertEqual(self.compound.created_by.username, 'username')

class PropertyTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='username',
            password='password123'
        )

        self.compound = Compound.objects.create(
            name='Voda',
            formula='H2O',
            area='inorg',
            mweight=18.02,
            created_by=self.user,
        )

        self.property = Property.objects.create(
            compound=self.compound,
            property_type= 'gst',
            value=1.05,
            unit= 'g/cm3',
            added_by=self.user
        )

    def test_propertycreatetest(self):
        self.assertEqual(self.property.property_type, 'gst')
        self.assertEqual(self.property.value, 1.05)
        self.assertEqual(self.property.unit, 'g/cm3')
        self.assertEqual(self.property.compound.name, 'Voda')

    def test_propertystr(self):
        # print(str(self.property))
        self.assertEqual(str(self.property), f"{self.compound.name} - gst")

    def test_propertytype(self):
        self.assertEqual(self.property.get_property_type_display(), 'gustina (g/cm3)')

class CategoryTest(TestCase):
    def setUp(self):
        pass

    def test_createcategory(self):
        category = Category.objects.create(name='Oksid')
        self.assertEqual(category.name, 'Oksid')
        self.assertEqual(str(category), 'Oksid')

class CommentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='username',
            password='password123'
        )

        self.compound = Compound.objects.create(
            name='Voda',
            formula='H2O',
            created_by=self.user,
        )

        self.comment = Coment.objects.create(
            compound=self.compound,
            user=self.user,
            text='text',
        )
    def test_createcomment(self):
        self.assertEqual(self.comment.text, 'text')
        self.assertEqual(self.compound.name, 'Voda')

###########FORME###################################
class CompoundFormTest(TestCase):
    def setUp(self):
        pass

    def test_compoundform(self):
        formdata = {'name': 'ugljen dioksid', 'formula': 'CO2', 'mweight': '48', 'area': 'inorg',}
        form = CompoundForm(data=formdata)
        self.assertTrue(form.is_valid())

    def testcompoundformnoname(self):
        formdata = { 'formula': 'CO2', 'mweight': '48', 'area': 'inorg',}
        form = CompoundForm(data=formdata)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_compoundformnoformula(self):
        formdata = {'name': 'ugljen dioksid',  'mweight': '48', 'area': 'inorg',}
        form = CompoundForm(data=formdata)
        self.assertFalse(form.is_valid())
        self.assertIn('formula', form.errors)

    def test_compoundformnoMW(self):
        formdata = {'name': 'ugljen dioksid', 'formula': 'CO2',  'area': 'inorg',}
        form = CompoundForm(data=formdata)
        # self.assertFalse(form.is_valid())
        # self.assertIn('mweight', form.errors)
        self.assertTrue(form.is_valid())

class PropertyFormTest(TestCase):
    def setUp(self):
        pass

    def test_propertyform(self):
        formdata = {'property_type': 'tt', 'value': -56.6, 'unit': '°C'}
        form = PropertyForm(data=formdata)
        self.assertTrue(form.is_valid())


    def test_propertyformnoproperty(self):
        formdata = { 'value': -56.6, 'unit': '°C'}
        form = PropertyForm(data=formdata)
        self.assertIn('property_type', form.errors)

    def test_propertyformnovalue(self):
        formdata = {'property_type': 'tt',  'unit': '°C'}
        form = PropertyForm(data=formdata)
        self.assertIn('value', form.errors)


    def test_propertyformnounit(self):
        formdata = {'property_type': 'tt', 'value': -56.6,}
        form = PropertyForm(data=formdata)
        # self.assertIn('unit', form.errors)
        self.assertTrue(form.is_valid())


################VIEWS##############################
class CompoundViewTest(TestCase):
    def setUp(self):
        self.cl = Client()
        self.user = User.objects.create_user(
            username='username',
            password='password123'
        )

        self.compound = Compound.objects.create(
            name='Voda',
            formula='H2O',
            area='inorg',
            mweight=18.02,
            created_by=self.user,
            public=True
        )

    def test_compoundlist(self):
        response = self.cl.get(reverse('compound_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Voda')
        self.assertTemplateUsed(response, 'core/compound_list.html')

    def test_compoundetail(self):
        response = self.cl.get(reverse('compound_detail', args=[self.compound.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Voda')
        self.assertTemplateUsed(response, 'core/compound_detail.html')

    def test_compoundcreate(self):
        success = self.cl.login(username='username', password='password123')
        self.assertTrue(success)
        response = self.cl.get(reverse('compound_create'))
        self.assertEqual(response.status_code, 200)

    def test_compoundUPDate(self):
        success = self.cl.login(username='username', password='password123')
        self.assertTrue(success)
        response = self.cl.get(reverse('compound_update', args=[self.compound.id]))
        self.assertEqual(response.status_code, 200)


    def test_compounddelete(self):
        success = self.cl.login(username='username', password='password123')
        self.assertTrue(success)
        response = self.cl.get(reverse('compound_delete', args=[self.compound.id]))
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.cl.get(reverse('compound_list'), {'search': 'Voda'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Voda')

# Create your tests here.
