from rest_framework import serializers
from .models import Exam, Question, QOPtion, ExamResult, Answer
from AuthenticationSystem.models import CustomUser


# ---------------------------------------------------------
# Serializer for question options
# Each option belongs to a specific question
# ---------------------------------------------------------
class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QOPtion
        fields = ["id", "option_content", "is_correct"]
        read_only_fields = ["is_correct"]  # Prevent users from modifying correctness


# ---------------------------------------------------------
# Serializer for questions
# Includes nested options so each question returns its options
# ---------------------------------------------------------
class QuestionSerializer(serializers.ModelSerializer):
    qOptions = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "question_content",
            "score",
            "question_number",
            "qOptions",
        ]


# ---------------------------------------------------------
# Basic exam serializer
# Used for listing exams without nested questions
# ---------------------------------------------------------
class ExamSerializer(serializers.ModelSerializer):
    creator = (
        serializers.StringRelatedField()
    )  # Display creator name instead of user id

    class Meta:
        model = Exam
        fields = [
            "id",
            "creator",
            "title",
            "description",
            "created_time",
            "updated_time",
            "question_many",
        ]


# ---------------------------------------------------------
# Full exam serializer
# Includes nested questions and their options
# Used when retrieving full exam details
# ---------------------------------------------------------
class ExamDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(source="question_set", many=True, read_only=True)

    class Meta:
        model = Exam
        fields = [
            "id",
            "creator",
            "title",
            "description",
            "created_time",
            "updated_time",
            "question_many",
            "questions",
        ]


# ---------------------------------------------------------
# Serializer for user answers to questions
# Used when submitting answers
# ---------------------------------------------------------
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            "id",
            "question",
            "selected_option",
            "is_correct",
        ]
        read_only_fields = ["is_correct"]


# ---------------------------------------------------------
# Serializer for creating exam results (submitting the exam)
# Includes nested answers for submission
# ---------------------------------------------------------
class ExamResultCreateSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = ExamResult
        fields = [
            "id",
            "user",
            "exam",
            "start_time",
            # "finish_time",
            "score",
            "answers",
        ]
        read_only_fields = ["score", "start_time", "finish_time"]

    # Overriding create to handle nested answers
    def create(self, validated_data):
        answers_data = validated_data.pop("answers")
        exam_result = ExamResult.objects.create(**validated_data)

        for ans in answers_data:
            Answer.objects.create(exam_result=exam_result, **ans)

        return exam_result


# ---------------------------------------------------------
# Serializer to view exam results after submission
# Includes answers and correctness
# ---------------------------------------------------------
class ExamResultDetailSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()
    exam = serializers.StringRelatedField()

    class Meta:
        model = ExamResult
        fields = [
            "id",
            "user",
            "exam",
            "start_time",
            # "finish_time",
            "score",
            "answers",
        ]
