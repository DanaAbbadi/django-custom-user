from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import CustomUser
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model




class CustomUserTest(TestCase):
    def setUp(self):
        self.email = 'dana123@gmail.com'
        self.password = 'D123456$'

    def test_signup_page_url_and_template(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='account/signup.html')

    def test_signup(self):
        response = self.client.post(reverse('account_signup'), data={
            'email': self.email,
            'password1': self.password,
        })
        self.assertEqual(response.status_code, 302)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)

    def test_duplicate_users(self):
        """
        Test if duplicate users are allowed by:
            1. Signup, after that you'll be redirected to home  
            2. Logout, you'll be redirected to home again.
            3. Signup again with the same user contact information. 
            4. No redirection, and response will contain 'A user is already registered with this e-mail address.'
            5. Test how many users are in the database, will be 1.
        """
        # Create first user
        response = self.client.post(reverse('account_signup'), data={
            'email': self.email,
            'password1': self.password,
        })

        # Check redirection to home, and number of users
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/')

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)

        # Logout
        logout_response = self.client.post(reverse('account_logout'))
        self.assertEqual(logout_response.status_code, 302)
        self.assertRedirects(logout_response, reverse('home'), status_code=302)

        # Signup with duplicate email
        response2 = self.client.post(reverse('account_signup'), data={
            'email': self.email,
            'password1': self.password,
        })

        # no redirection, still in signup page
        self.assertTemplateUsed(response2, template_name='account/signup.html')
        self.assertContains(response2,'A user is already registered with this e-mail address.')

        # users.count equals 1 not 2, since signup failed
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)