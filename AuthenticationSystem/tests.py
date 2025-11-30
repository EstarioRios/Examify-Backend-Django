# ----------------------------
# Comprehensive tests for AuthenticationSystem app
# Includes: singin, login, manual_login
# Covers success and failure cases
# ----------------------------

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from AuthenticationSystem.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


# ----------------------------
# Base setup for auth tests
# ----------------------------
class AuthBaseSetup(APITestCase):
    def setUp(self):
        # ----------------------------
        # Create initial users
        # ----------------------------
        self.teacher_user = CustomUser.objects.create_teacher(
            first_name="John",
            last_name="Doe",
            user_name="teacher1",
            password="pass1234",
        )
        self.student_user = CustomUser.objects.create_student(
            first_name="Jane",
            last_name="Doe",
            user_name="student1",
            password="pass1234",
        )

        # ----------------------------
        # Setup API clients
        # ----------------------------
        self.client_teacher = APIClient()
        self.client_student = APIClient()

        # JWT Tokens
        self.teacher_token = str(RefreshToken.for_user(self.teacher_user).access_token)
        self.student_token = str(RefreshToken.for_user(self.student_user).access_token)

        # Authenticated clients
        self.client_teacher.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.teacher_token}"
        )
        self.client_student.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.student_token}"
        )


# ----------------------------
# Singin Tests
# ----------------------------
class SigninTests(AuthBaseSetup):

    # Student signup success
    def test_student_singin_success(self):
        data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "user_name": "alice123",
            "user_type": "student",
            "password": "pass5678",
        }
        response = self.client_student.post(reverse("singin"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)

    # Teacher signup success
    def test_teacher_singin_success(self):
        data = {
            "first_name": "Bob",
            "last_name": "Smith",
            "user_name": "bob123",
            "user_type": "teacher",
            "password": "pass5678",
        }
        response = self.client_teacher.post(reverse("singin"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)

    # Fail: missing fields
    def test_singin_missing_fields_fail(self):
        data = {"first_name": "Alice"}
        response = self.client_student.post(reverse("singin"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Fail: username already exists
    def test_singin_username_exists_fail(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "user_name": "teacher1",
            "user_type": "teacher",
            "password": "pass1234",
        }
        response = self.client_teacher.post(reverse("singin"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# ----------------------------
# Manual Login Tests
# ----------------------------
class ManualLoginTests(AuthBaseSetup):

    # Success: correct credentials with remember True
    def test_manual_login_success_remember_true(self):
        data = {
            "id_code": self.student_user.id_code,
            "password": "pass1234",
            "remember": True,
        }
        response = self.client_student.post(reverse("manual_login"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tokens", response.data)

    # Success: correct credentials with remember False
    def test_manual_login_success_remember_false(self):
        data = {
            "id_code": self.student_user.id_code,
            "password": "pass1234",
            "remember": False,
        }
        response = self.client_student.post(reverse("manual_login"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("tokens", response.data)

    # Fail: wrong password
    def test_manual_login_wrong_password_fail(self):
        data = {"id_code": self.student_user.id_code, "password": "wrongpass"}
        response = self.client_student.post(reverse("manual_login"), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Fail: user does not exist
    def test_manual_login_user_not_found_fail(self):
        data = {"id_code": 9999, "password": "pass1234"}
        response = self.client_student.post(reverse("manual_login"), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Fail: missing fields
    def test_manual_login_missing_fields_fail(self):
        data = {"id_code": self.student_user.id_code}
        response = self.client_student.post(reverse("manual_login"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ----------------------------
# JWT Login Tests
# ----------------------------
class JWTLoginTests(AuthBaseSetup):

    # Success: valid JWT
    def test_login_success_jwt(self):
        response = self.client_student.post(reverse("login"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user_type", response.data)

    # Fail: invalid JWT
    def test_login_fail_invalid_jwt(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer invalidtoken")
        response = client.post(reverse("login"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["msg"], "your JWT isn't fine")
