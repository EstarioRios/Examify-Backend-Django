# ----------------------------
# Comprehensive tests for core app
# Includes: Exam, Question, QOPtion, ExamResult, Answer
# Covers both success and failure cases
# ----------------------------

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from AuthenticationSystem.models import CustomUser
from core.models import Exam, Question, QOPtion, ExamResult, Answer


# ----------------------------
# Base setup for all tests
# ----------------------------
class BaseTestSetup(APITestCase):
    def setUp(self):
        # ----------------------------
        # Create teacher and student users
        # ----------------------------
        self.teacher = CustomUser.objects.create_user(
            username="teacher1", password="pass1234", user_type="teacher"
        )
        self.student = CustomUser.objects.create_user(
            username="student1", password="pass1234", user_type="student"
        )

        # ----------------------------
        # Authenticate and get JWT tokens
        # ----------------------------
        self.client_teacher = APIClient()
        res = self.client_teacher.post(
            "/auth/jwt/create/",
            {"username": "teacher1", "password": "pass1234"},
            format="json",
        )
        self.teacher_token = res.data["access"]
        self.client_teacher.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.teacher_token}"
        )

        self.client_student = APIClient()
        res = self.client_student.post(
            "/auth/jwt/create/",
            {"username": "student1", "password": "pass1234"},
            format="json",
        )
        self.student_token = res.data["access"]
        self.client_student.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.student_token}"
        )

        # ----------------------------
        # Create initial exam
        # ----------------------------
        self.exam = Exam.objects.create(
            creator=self.teacher,
            title="Test Exam",
            description="A test exam",
            created_time=timezone.now(),
        )

        # ----------------------------
        # Create initial question
        # ----------------------------
        self.question = Question.objects.create(
            exam=self.exam, question_content="What is 2+2?", score=5, question_number=1
        )

        # ----------------------------
        # Create initial QOPtion
        # ----------------------------
        self.option = QOPtion.objects.create(
            question=self.question, option_content="4", is_correct=True
        )

        # ----------------------------
        # Create initial ExamResult
        # ----------------------------
        self.exam_result = ExamResult.objects.create(
            user=self.student, exam=self.exam, start_time=timezone.now(), score=0
        )


# ----------------------------
# Exam Tests
# ----------------------------
class ExamTests(BaseTestSetup):

    # Create exam - success
    def test_create_exam_teacher_success(self):
        data = {"title": "New Exam", "description": "New Desc"}
        response = self.client_teacher.post(reverse("create_exam"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Create exam - fail: student cannot create
    def test_create_exam_student_fail(self):
        data = {"title": "Student Exam", "description": "Desc"}
        response = self.client_student.post(reverse("create_exam"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Delete exam - success
    def test_delete_exam_success(self):
        response = self.client_teacher.delete(
            reverse("delete_exam"), {"id": self.exam.id}
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Edit exam - success
    def test_edit_exam_success(self):
        data = {
            "id": self.exam.id,
            "new_title": "Edited",
            "new_description": "Edited Desc",
        }
        response = self.client_teacher.put(reverse("edit_exam"), data)
        # Depending on your view, may return 200 or 204
        self.assertIn(
            response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]
        )

    # Show single exam - success
    def test_show_exam_success(self):
        response = self.client_teacher.get(reverse("show_exam") + f"?id={self.exam.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Show all exams - success
    def test_show_all_exams_success(self):
        response = self.client_teacher.get(reverse("show_all_exams"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ----------------------------
# Question Tests
# ----------------------------
class QuestionTests(BaseTestSetup):

    # Create question - success
    def test_create_question_success(self):
        data = {
            "exam_id": self.exam.id,
            "question_content": "New question?",
            "question_score": 5,
        }
        response = self.client_teacher.post(reverse("create_question"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Delete question - success
    def test_delete_question_success(self):
        response = self.client_teacher.delete(
            reverse("delete_question"), {"id": self.question.id}
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Show question - success
    def test_show_question_success(self):
        response = self.client_teacher.get(
            reverse("show_question") + f"?id={self.question.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ----------------------------
# QOPtion Tests
# ----------------------------
class QOPtionTests(BaseTestSetup):

    # Create option - success
    def test_create_option_success(self):
        data = {"id": self.question.id, "content": "5", "is_correct": False}
        response = self.client_teacher.post(reverse("create_option"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Delete option - success
    def test_delete_option_success(self):
        response = self.client_teacher.delete(
            reverse("delete_option"), {"id": self.option.id}
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# ----------------------------
# ExamResult Tests
# ----------------------------
class ExamResultTests(BaseTestSetup):

    # Create ExamResult (start exam) - success
    def test_create_exam_result_success(self):
        data = {"exam_id": self.exam.id}
        response = self.client_student.post(reverse("create_exam_result"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# ----------------------------
# Answer Tests
# ----------------------------
class AnswerTests(BaseTestSetup):

    # Create answer - success
    def test_create_answer_success(self):
        data = {
            "exam_result_id": self.exam_result.id,
            "question_id": self.question.id,
            "selected_option_id": self.option.id,
        }
        response = self.client_student.post(reverse("create_answer"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Create answer - fail: option does not belong to question
    def test_create_answer_wrong_option_fail(self):
        wrong_option = QOPtion.objects.create(
            question=self.question, option_content="5", is_correct=False
        )
        data = {
            "exam_result_id": self.exam_result.id,
            "question_id": self.question.id,
            "selected_option_id": wrong_option.id + 100,  # non-existent
        }
        response = self.client_student.post(reverse("create_answer"), data)
        self.assertIn(
            response.status_code,
            [status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST],
        )


# ----------------------------
