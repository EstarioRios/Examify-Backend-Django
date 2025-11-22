from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone

# --------------------

from .models import Exam, Question, QOPtion
from .serializers import ExamSerializer, QuestionSerializer, QOPtionSerializer

# --------------------


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_exma(request):
    try:
        user_auth = JWTAuthentication().authenticate(request)
        if not user_auth:
            return Response(
                {"error": "your JWT isn't fine"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            user, _ = user_auth
    except AuthenticationFailed:
        return Response(
            {"error": "your JWT isn't fine"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    exam_title = request.data.get("title")
    exma_description = request.data.get("description")
    exam_creator = user

    if not all([exam_title, exma_description, exam_creator]):
        return Response(
            {"error": "all fields (title, description, creator) are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if user.user_type != "teacher":
        return Response(
            {"error", "you aren't allowed"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if Exam.objects.filter(title=exam_title).exists():
        return Response(
            {"error": "title is already exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        exam = Exam.objects.create(
            title=exam_title,
            description=exma_description,
            creator=exam_creator,
        )
        exam.save(using=_db)
        return Response(status=status.HTTP_201_CREATED)

    except ValueError as e:
        return Response(
            {"error": f"{e}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_exam(request):
    try:
        user_auth = JWTAuthentication().authenticate(request)
        if not user_auth:
            return Response(
                {"error": "your JWT isn't fine"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, _ = user_auth
    except AuthenticationFailed:
        return Response(
            {"error": "your JWT isn't fine"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    exam_id = request.data.get("id")

    if not exam_id:
        return Response(
            {"error": "field id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not Exam.objects.filter(id=exam_id).exists():
        return Response(
            {"error": f"exam by id {exam_id} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    target_exam = Exam.objects.get(id=exam_id)

    if not target_exam.creator == user:
        return Response(
            {"error": "you aren't allowed"},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        target_exam.delete()

        return Response(status=status.HTTP_200_OK)
    except ValueError as e:
        return Response(
            {"error": f"{e}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_exam(request):
    try:
        user_auth = JWTAuthentication().authenticate(request)
        if not user_auth:
            return Response(
                {"error": "your JWT isn't fine"},
                status=status.HTTP_400_BAD_REQUEST,
            )

            user, _ = user_auth
    except AuthenticationFailed:
        return Response(
            {"error": "your JWT isn't fine"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    exam_id = request.data.get("id")

    if not exam_id:
        return Response(
            {"error": "field id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not Exam.objects.filter(id=exam_id).exists():
        return Response(
            {"error": f"exam by id {exam_id} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    new_title = request.data.get("new_title")
    new_description = request.data.get("new_description")
    new_updated_time = timezone.now()

    try:
        target_exam = Exam.objects.get(id=exam_id)

    except ValueError as e:
        return Response(
            {"error": f"{e}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not target_exam.creator == user:
        return Response(
            {"error": "you aren't allowed"},
            status=status.HTTP_403_FORBIDDEN,
        )


# --------------------


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_question(request):
    try:
        user_auth = JWTAuthentication().authenticate(request)
        if not user_auth:
            return Response(
                {"error": "your JWT isn't fine"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, _ = user_auth

    except AuthenticationFailed:
        return Response(
            {"error": "your JWT isn't fine"},
            status=status.HTTP_400_BAD_REQUEST,
        )

        exam_id = request.data.get("exam_id")
        question_content = request.data.get("question_content")
        question_score = request.data.get("question_score")

        if not all([exam_id, question_content, question_content]):
            return Response(
                {
                    "error": "all fields (exam_id, question_content, question_score) are required"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not Exam.objects.filter(id=exam_id).exists():
            return Response(
                {"error": f"exam by id {exam_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        target_exam = Exam.objects.get(id=exam_id)

        if not target_exam.creator == user:
            return Response(
                {"error": "you aren't allowed"},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            question = Question.objects.create(
                exam=target_exam,
                question_content=question_content,
                score=question_score,
            )
            question.save()
            return Response(status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response(
                {"error": f"{e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_question(request):
    try:
        user_auth = JWTAuthentication().authenticate(request)
        if not user_auth:
            return Response(
                {"error": "your JWT isn't fine"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, _ = user_auth
    except AuthenticationFailed:
        return Response(
            {"error": "your JWT isn't fine"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    question_id = request.data.get("id")
    if not question_id:
        return Response(
            {"error": "field id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

        if not Question.objects.filter(id=question_id).exists():
            return Response(
                {"error": f"question by id {question_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        target_question = Question.objects.get(id=question_id)
        t_q_e = target_question.exam
        t_q_e_creator = t_q_e.creator

        if not t_q_e_creator == user:
            return Response(
                {"error": "your aren't allowed"},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            target_question.delete()
            return Response(status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {"error": f"{e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
