# In your_app_name/tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from django.db.utils import IntegrityError # Import IntegrityError for testing uniqueness constraints

class CustomUserModelTests(TestCase):

    # Helper method to get the custom user model
    def get_user_model(self):
        return get_user_model()

    # Define common user data for testing
    def setUp(self):
        self.email = "normaluser@example.com"
        self.username = "normaluser"
        self.first_name = "Normal"
        self.last_name = "User"
        self.password = "password123"

        self.superuser_email = "superuser@example.com"
        self.superuser_username = "superuser"
        self.superuser_first_name = "Super"
        self.superuser_last_name = "User"
        self.superuser_password = "superpassword123"


    def test_create_user_with_required_fields(self):
        """
        Tests creating a normal user with email as USERNAME_FIELD
        and other required fields (username, first_name, last_name).
        """
        User = self.get_user_model()
        user = User.objects.create_user(
            email=self.email,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password
        )

        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password(self.password)) # Verify password is set correctly


    def test_create_user_missing_required_fields(self):
        """
        Tests that creating a user fails if any required field is missing.
        We expect a ValueError from our custom manager's validation.
        """
        User = self.get_user_model()

        # Test missing email
        with self.assertRaisesMessage(ValueError, "The Email must be set"):
             User.objects.create_user(
                email="", # Or None
                username=self.username,
                first_name=self.first_name,
                last_name=self.last_name,
                password=self.password
             )

         # Test missing username
        with self.assertRaisesMessage(ValueError, "The Username must be set"):
             User.objects.create_user(
                email=self.email,
                username="", # Or None
                first_name=self.first_name,
                last_name=self.last_name,
                password=self.password
             )

        # Test missing first_name
        with self.assertRaisesMessage(ValueError, "The First Name must be set"):
             User.objects.create_user(
                email=self.email,
                username=self.username,
                first_name="", # Or None
                last_name=self.last_name,
                password=self.password
             )

         # Test missing last_name
        with self.assertRaisesMessage(ValueError, "The Last Name must be set"):
             User.objects.create_user(
                email=self.email,
                username=self.username,
                first_name=self.first_name,
                last_name="", # Or None
                password=self.password
             )

    def test_email_is_unique(self):
        """
        Tests that creating a user with a duplicate email fails.
        We expect an IntegrityError from the database constraint.
        """
        User = self.get_user_model()
        User.objects.create_user(
            email=self.email,
            username="user1", # Different username is fine
            first_name="User",
            last_name="One",
            password=self.password
        )
        # Attempt to create another user with the same email
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email=self.email, # Duplicate email
                username="user2",
                first_name="User",
                last_name="Two",
                password=self.password
            )

    def test_username_is_unique(self):
        """
        Tests that creating a user with a duplicate username fails.
        We expect an IntegrityError from the database constraint.
        """
        User = self.get_user_model()
        User.objects.create_user(
            email="user1@example.com",
            username=self.username, # Duplicate username
            first_name="User",
            last_name="One",
            password=self.password
        )
        # Attempt to create another user with the same username
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="user2@example.com",
                username=self.username, # Duplicate username
                first_name="User",
                last_name="Two",
                password=self.password
            )


    def test_create_superuser(self):
        """
        Tests creating a superuser with all required fields.
        """
        User = self.get_user_model()
        superuser = User.objects.create_superuser(
            email=self.superuser_email,
            username=self.superuser_username,
            first_name=self.superuser_first_name,
            last_name=self.superuser_last_name,
            password=self.superuser_password
        )

        self.assertIsNotNone(superuser)
        self.assertEqual(superuser.email, self.superuser_email)
        self.assertEqual(superuser.username, self.superuser_username)
        self.assertEqual(superuser.first_name, self.superuser_first_name)
        self.assertEqual(superuser.last_name, self.superuser_last_name)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password(self.superuser_password))


    def test_create_superuser_missing_flags(self):
        """
        Tests that creating a superuser fails if is_staff or is_superuser is False.
        We expect a ValueError from our custom manager's validation.
        """
        User = self.get_user_model()

        # Test missing is_staff
        with self.assertRaisesMessage(ValueError, "Superuser must have is_staff=True."):
            User.objects.create_superuser(
                email=self.superuser_email,
                username=self.superuser_username,
                first_name=self.superuser_first_name,
                last_name=self.superuser_last_name,
                password=self.superuser_password,
                is_staff=False # Should fail
            )

        # Test missing is_superuser
        with self.assertRaisesMessage(ValueError, "Superuser must have is_superuser=True."):
            User.objects.create_superuser(
                email=self.superuser_email,
                username=self.superuser_username,
                first_name=self.superuser_first_name,
                last_name=self.superuser_last_name,
                password=self.superuser_password,
                is_superuser=False # Should fail
            )

    def test_authenticate_user_with_email_and_password(self):
        """
        Tests that a user can authenticate using their email and password
        via the custom backend.
        """
        User = self.get_user_model()
        user = User.objects.create_user(
            email=self.email,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password
        )

        # Authenticate using email (as username argument) and password
        # Note: authenticate expects 'username' and 'password' args by default,
        # but our custom backend looks up by the 'username' arg which we pass the email into.
        authenticated_user = authenticate(username=self.email, password=self.password)

        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user, user) # Check if it's the correct user object

    def test_authenticate_user_with_incorrect_password(self):
        """
        Tests that authentication fails with the correct email but incorrect password.
        """
        User = self.get_user_model()
        User.objects.create_user(
            email=self.email,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password
        )

        # Authenticate with wrong password
        authenticated_user = authenticate(username=self.email, password="wrongpassword")

        self.assertIsNone(authenticated_user) # Authentication should fail


    def test_authenticate_non_existent_user(self):
        """
        Tests that authentication fails for a non-existent email address.
        """
        # No user created

        # Attempt to authenticate with a non-existent email
        authenticated_user = authenticate(username="nonexistent@example.com", password="somepassword")

        self.assertIsNone(authenticated_user) # Authentication should fail


    def test_authenticate_user_with_username_only_fails(self):
        """
        Tests that authentication fails if only username (not email) is provided,
        assuming the EmailBackend is used or ordered before ModelBackend.
        If ModelBackend is also active and ordered first, this test might need adjustment.
        This tests that the custom backend doesn't authenticate purely by username.
        """
        User = self.get_user_model()
        User.objects.create_user(
            email=self.email,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password
        )

        # Attempt to authenticate using username instead of email
        authenticated_user = authenticate(username=self.username, password=self.password)

        # It should fail because our EmailBackend looks for email matching the 'username' arg
        # and the default ModelBackend might be disabled or checked later.
        # If ModelBackend is active and first, this test needs adjustment.
        # Assuming EmailBackend is primary:
        self.assertIsNone(authenticated_user)

    def test_username_field_is_email(self):
        """
        Tests that the USERNAME_FIELD is correctly set to 'email'.
        """
        User = self.get_user_model()
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_required_fields(self):
         """
         Tests that REQUIRED_FIELDS is correctly set.
         """
         User = self.get_user_model()
         self.assertEqual(User.REQUIRED_FIELDS, ['username', 'first_name', 'last_name']) # Order might not strictly matter, but good to match