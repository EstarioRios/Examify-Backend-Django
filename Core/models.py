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
    updated_time = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )

    question_many = models.IntegerField(default=0, null=False, blank=False)


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=False, blank=False)
    question_content = models.TextField(null=False, blank=False)
    score = models.DecimalField(
        null=False,
        blank=False,
        decimal_places=2,
        max_digits=4,
        default=0.00,
    )

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


class ExamResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    start_time = models.DateTimeField(auto_now_add=True)
    # finish_time = models.DateTimeField(null=True, blank=True)

    score = models.DecimalField(
        null=False,
        blank=False,
        default=0.00,
        decimal_places=2,
        max_digits=4,
    )

    def __str__(self):
        return f"{self.user} - {self.exam} - {self.score}"


class Answer(models.Model):
    exam_result = models.ForeignKey(
        ExamResult, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QOPtion, on_delete=models.CASCADE)

    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.is_correct = self.selected_option.is_correct
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.question} -> {self.selected_option}"
