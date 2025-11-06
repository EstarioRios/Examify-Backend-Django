from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# --------------------

from .models import Exam, Question, QOPtion
from .serializers import ExamSerializer, QuestionSerializer, QOPtionSerializer

# --------------------


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def no():
    pass
