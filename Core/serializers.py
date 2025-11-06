from rest_framework.serializers import ModelSerializer
from .models import Exam, Question, QOPtion


class ExamSerializer(ModelSerializer):
    class Meta:
        model = Exam
        fields = [
            "title",
            "description",
            "created_time",
            "creator",
            "updated_time",
            "question_many",
            "qOptions",
        ]


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = [
            # "question_type",
            "question_content",
            "question_number",
        ]


class QOPtionSerializer(ModelSerializer):
    class Meta:
        model = QOPtion
        fields = [
            "option_content",
            "is_correct",
        ]
