from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import CustomUser
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model




class CustomUserTest(TestCase):
    def setUp(self):
        self.username = 'dana123'
        self.email = 'dana123@gmail.com'
        self.password = 'D123456$'

    def test_signup_page_url_and_template(self):
        response = self.client.get("/users/signup/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/signup.html')

    def test_signup(self):
        response = self.client.post(reverse('signup'), data={
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 302)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)

        response1 = self.client.post(reverse('login'), data={
            'username': self.username,
            'password1': self.password,
        })
        self.assertEqual(response1.status_code, 200)
        self.assertContains(response1, 'dana123')

    def test_duplicate_users(self):
        """
        Test if duplicate users are allowed by:
            1. Creat an initial user, then sign in. 
            2. Signup again with the same user contact information.
            3. Test if the page is redirected to login page. 
            3. Test how many users are in the database.
        """
        response = self.client.post(reverse('signup'), data={
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 302)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)

        response1 = self.client.post(reverse('login'), data={
            'username': self.username,
            'password1': self.password,
        })
        self.assertEqual(response1.status_code, 200)
        self.assertContains(response1, 'dana123')

        response2 = self.client.post(reverse('signup'), data={
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        })
        # status code is 200 not 302, since signup failed so there is no direction to signin page
        self.assertEqual(response2.status_code, 200)
        # users.count equals 1 not 2, since signup failed
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)





