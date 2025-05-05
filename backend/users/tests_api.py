# users/tests_api.py

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAPITests(APITestCase):

    def setUp(self):
        # Create a user that can be used for login/authenticated requests
        self.user_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword123'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token, created = Token.objects.get_or_create(user=self.user)

        # Define URLs for easy access
        self.register_url = reverse('user-register')
        self.login_url = reverse('user-login')
        self.logout_url = reverse('user-logout')
        self.me_url = reverse('current-user')


    # --- Registration Tests ---

    def test_registration_success(self):
        """
        Ensure we can register a new user successfully.
        """
        new_user_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpassword123'
        }
        response = self.client.post(self.register_url, new_user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2) # Check if a new user is created
        # Verify the new user exists in the database
        new_user = User.objects.get(email='newuser@example.com')
        self.assertEqual(new_user.username, 'newuser')
        self.assertEqual(new_user.first_name, 'New')
        self.assertEqual(new_user.last_name, 'User')
        self.assertTrue(new_user.check_password('newpassword123')) # Check if password is hashed


    def test_registration_missing_required_fields(self):
        """
        Ensure registration fails with missing required fields.
        """
        # Missing email
        missing_email_data = {
             'username': 'failuser',
             'first_name': 'Fail',
             'last_name': 'User',
             'password': 'password'
        }
        response = self.client.post(self.register_url, missing_email_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data) # Check if 'email' field error is returned


        # Missing username
        missing_username_data = {
             'email': 'failuser@example.com',
             'first_name': 'Fail',
             'last_name': 'User',
             'password': 'password'
        }
        response = self.client.post(self.register_url, missing_username_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data) # Check if 'username' field error is returned

        # ... Add checks for missing first_name, last_name, and password ...
        # Missing first_name
        missing_first_name_data = {
             'email': 'failuser@example.com',
             'username': 'failuser',
             'last_name': 'User',
             'password': 'password'
        }
        response = self.client.post(self.register_url, missing_first_name_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)

         # Missing last_name
        missing_last_name_data = {
             'email': 'failuser@example.com',
             'username': 'failuser',
             'first_name': 'Fail',
             'password': 'password'
        }
        response = self.client.post(self.register_url, missing_last_name_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('last_name', response.data)

        # Missing password
        missing_password_data = {
             'email': 'failuser@example.com',
             'username': 'failuser',
             'first_name': 'Fail',
             'last_name': 'User',
        }
        response = self.client.post(self.register_url, missing_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)


        self.assertEqual(User.objects.count(), 1) # Ensure no new user was created


    def test_registration_duplicate_email(self):
        """
        Ensure registration fails with a duplicate email.
        """
        duplicate_email_data = {
            'email': self.user_data['email'], # Use existing email
            'username': 'anotheruser',
            'first_name': 'Another',
            'last_name': 'User',
            'password': 'anotherpassword'
        }
        response = self.client.post(self.register_url, duplicate_email_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data) # Check for email uniqueness error
        self.assertEqual(User.objects.count(), 1) # Ensure no new user was created


    def test_registration_duplicate_username(self):
        """
        Ensure registration fails with a duplicate username.
        """
        duplicate_username_data = {
            'email': 'anotheruser@example.com',
            'username': self.user_data['username'], # Use existing username
            'first_name': 'Another',
            'last_name': 'User',
            'password': 'anotherpassword'
        }
        response = self.client.post(self.register_url, duplicate_username_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data) # Check for username uniqueness error
        self.assertEqual(User.objects.count(), 1) # Ensure no new user was created


    # --- Login Tests ---

    def test_login_success(self):
        """
        Ensure a user can log in with correct credentials (email and password).
        """
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data) # Check that a token is returned
        self.assertIn('user', response.data)  # Check that user data is returned
        self.assertEqual(response.data['user']['email'], self.user.email)
        # Do NOT check for password in response data
        self.assertNotIn('password', response.data['user'])


    def test_login_incorrect_password(self):
        """
        Ensure login fails with incorrect password.
        """
        login_data = {
            'email': self.user_data['email'],
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid credentials.')


    def test_login_non_existent_email(self):
        """
        Ensure login fails for a non-existent email.
        """
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'anypassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid credentials.')


    def test_login_inactive_user(self):
        """
        Ensure login fails for an inactive user.
        """
        inactive_user_data = {
            'email': 'inactiveuser@example.com',
            'username': 'inactiveuser',
            'first_name': 'Inactive',
            'last_name': 'User',
            'password': 'password'
        }
        inactive_user = User.objects.create_user(**inactive_user_data)
        inactive_user.is_active = False
        inactive_user.save()

        login_data = {
            'email': inactive_user_data['email'],
            'password': inactive_user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'User account is disabled.')


    # --- Current User Tests (/me/) ---

    def test_get_current_user_authenticated(self):
        """
        Ensure authenticated user can fetch their own details via /me/.
        """
        # Authenticate the client using the token from setUp
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.get(self.me_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['username'], self.user.username)
        # Do NOT check for password in response data
        self.assertNotIn('password', response.data)


    def test_get_current_user_unauthenticated(self):
        """
        Ensure unauthenticated user cannot fetch details via /me/.
        """
        # Client is not authenticated by default

        response = self.client.get(self.me_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')


     # --- Logout Tests ---

    def test_logout_authenticated(self):
        """
        Ensure authenticated user can log out (token is deleted).
        """
        # Authenticate the client using the token from setUp
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Check that the token exists before logout
        self.assertTrue(Token.objects.filter(user=self.user).exists())

        response = self.client.post(self.logout_url, format='json') # POST to logout

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Successfully logged out.')

        # Check that the token has been deleted
        self.assertFalse(Token.objects.filter(user=self.user).exists())

        # Attempt to access a protected endpoint with the old token
        response_after_logout = self.client.get(self.me_url, format='json')
        self.assertEqual(response_after_logout.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_logout_unauthenticated(self):
        """
        Ensure unauthenticated user cannot access logout.
        """
        # Client is not authenticated by default

        response = self.client.post(self.logout_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)