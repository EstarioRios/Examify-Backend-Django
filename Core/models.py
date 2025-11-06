from django.db import models
from django.contrib.auth import get_user_model
from AuthenticationSystem.models import CustomUser


class Exam(models.Model):
    creator = models.ForeignKey(
        to=CustomUser, on_delete=models.CASCADE, null=False, blank=False
    )
    title = models.CharField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    created_time = models.DateTimeField(auto_now_add=False)
    updated_time = models.DateTimeField(auto_now=False, auto_now_add=False)

    question_many = models.IntegerField(default=0, null=False, blank=False)


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=False, blank=False)
    question_content = models.TextField(null=False, blank=False)

    # QUESTION_TYPES = [
    #     ("text", "Text Answer"),
    #     ("radio", "Single Choice"),
    #     ("check_box", "Multiple Choice"),
    # ]

    question_number = models.IntegerField(null=False, blank=False)

    # question_type = models.CharField(
    #     choices=QUESTION_TYPES, default="text", null=False, blank=False
    # )

    def __str__(self):
        return self.question_content


class QOPtion(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="qOptions",
    )

    option_content = models.CharField(null=False, blank=False)
    is_correct = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return self.option_content
