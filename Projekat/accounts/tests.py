from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

User = get_user_model()
#########################NODELS######################################################
class CustomuserTest(TestCase):

    def test_createuser(self):
        user = User.objects.create_user(username='username',  email='email@test.com', password='password123')
        self.assertEqual(user.username, 'username')
        self.assertEqual(user.email, 'email@test.com')
        self.assertTrue(user.check_password('password123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_createsuperuser(self):
        user = User.objects.create_superuser(username='admin', password='password123', email='admin@test.com')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

#############VIEWS##################################################################
class ViewsTest(TestCase):
    def setUp(self):
        self.cl = Client()
        self.user = User.objects.create(
            username='username',
            password='password123',
            email='email@test.com'
        )

    def test_regviewget(self):
        response = self.cl.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_regviewpost(self):
        response = self.cl.post(reverse('register'), {'username': 'user','email': 'email@test.com','password1': 'password123','password2': 'password123'})
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(User.objects.filter(username='username').exists())

    def test_loginviewget(self):
        response = self.cl.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_loginview_post(self):
        response = self.cl.post(reverse('login'), {'username': 'username','password': 'password123'})
        self.assertIn(response.status_code, [200, 302])
# Create your tests here.
