from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone

# --------------------

from .models import Exam, Question, QOPtion, ExamResult, Answer
from .serializers import (
    ExamSerializer,
    QuestionSerializer,
    QOPtionSerializer,
    AnswerSerializer,
    ExamResultDetailSerializer,
    # ExamResultCreateSerializer,
)

# --------------------


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_exam(request):
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
    exam_description = request.data.get("description")
    exam_creator = user

    if not all([exam_title, exam_description, exam_creator]):
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
            description=exam_description,
            creator=exam_creator,
        )
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

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
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

    if not all([exam_id, question_content, question_score]):
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
        exam_question_many = target_exam.question_many
        new_exam_question_many = int(exam_question_many) + 1
        target_exam.question_many = new_exam_question_many
        target_exam.save()
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
            {"error": "you aren't allowed"},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        exam_of_target_question = target_question.exam
        many_question_of_exam = exam_of_target_question.question_many
        new_many_question_of_exam = int(many_question_of_exam) - 1
        exam_of_target_question.question_many = new_many_question_of_exam
        exam_of_target_question.save()

        target_question.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    except ValueError as e:
        return Response(
            {"error": f"{e}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_option(request):
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
    option_content = request.data.get("content")
    is_correct = bool(request.data.get("is_correct"))

    if not is_correct:
        is_correct = False

    if not all([question_id, option_content]):
        return Response(
            {"error": "all fields (id, content) are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not Question.objects.filter(id=question_id).exists():
        return Response(
            {"error": f"question by id {question_id} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    exam_owner = Question.objects.get(id=question_id).exam.creator

    if not exam_owner == user:
        return Response(
            {"error": "you aren't allowed"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if QOPtion.objects.filter(
        question=Question.objects.get(id=question_id), is_correct=True
    ).exists():
        return Response(
            {"error": "there are a correct qoption already"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        q_option = QOPtion.objects.create(
            question=Question.objects.get(id=question_id),
            option_content=option_content,
            is_correct=is_correct,
        )

        return Response(
            status=status.HTTP_201_CREATED,
        )
    except ValueError as e:
        return Response(
            {"error": f"{e}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_option(request):
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

    option_id = request.data.get("id")
    if not option_id:
        return Response(
            {"error": "field id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not QOPtion.objects.filter(id=option_id).exists():
        return Response(
            {"error": f"qoption by id {option_id} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    target_qoption = QOPtion.objects.get(id=option_id)

    if not user == target_qoption.question.exam.creator:
        return Response(
            {"error": "you aren't allowed"},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        target_qoption.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
    except ValueError as e:
        return Response(
            {"error": f"{e}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def show_exam(request):
    exam_id = request.query_params.get("id")
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

    return Response(
        {"exam": ExamSerializer(Exam.objects.get(id=exam_id)).data},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def show_all_exams(request):

    try:
        return Response(
            {"exams": ExamSerializer(Exam.objects.all(), many=True).data},
            status=status.HTTP_200_OK,
        )
    except ValueError as e:
        return Response(
            {"error": f"{e}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def show_question(request):
    question_id = request.query_params.get("id")

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

    return Response(
        {"question": QuestionSerializer(Question.objects.get(id=question_id)).data},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_exam_result(request):
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

    target_exam_id = request.data.get("exam_id")
    if not target_exam_id:
        return Response(
            {"error": "field exam_id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not Exam.objects.filter(id=target_exam_id).exists():
        return Response(
            {"error": f"exam by id {target_exam_id} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:

        started_time = timezone.now()
        exam_result_instance = ExamResult.objects.create(
            user=user,
            exam=Exam.objects.get(id=target_exam_id),
            start_time=started_time,
        )
        return Response(
            status=status.HTTP_201_CREATED,
        )
    except ValueError as e:
        return Response(
            {"error": f"{e}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_answer(request):
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

    exam_result_id = request.data.get("exam_result_id")
    question_id = request.data.get("question_id")
    selected_option_id = request.data.get("selected_option_id")
    # is_correct_question = None

    if not all([exam_result_id, question_id, selected_option_id]):
        return Response(
            {
                "error": "all field (exam_result_id, question_id, selected_option_id) are required"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not ExamResult.objects.filter(id=exam_result_id).exists():
        return Response(
            {"error": f"exam_result by id {exam_result_id} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if not Question.objects.filter(id=question_id).exists():
        return Response(
            {"error": f"question by id {question_id} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if not QOPtion.objects.filter(id=selected_option_id).exists():
        return Response(
            {"error": f"option by id {selected_option_id} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        exam_result = ExamResult.objects.get(id=exam_result_id)
        question = Question.objects.get(id=question_id)
        selected_option = QOPtion.objects.get(id=selected_option_id)
    except ValueError as e:
        return Response(
            {"error": f"{e}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if selected_option.question.id != question.id:
        return Response(
            {"error": "selected option does not belong to the question"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        answer_instance = Answer.objects.create(
            exam_result=exam_result,
            question=question,
            selected_option=selected_option,
            is_correct=bool(selected_option.is_correct),
        )
        return Response(
            status=status.HTTP_201_CREATED,
        )
    except ValueError as e:
        return Response(
            {"error": f"{e}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
