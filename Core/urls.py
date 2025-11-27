from django.urls import path
from . import views

urlpatterns = [
    # Exam
    path("exam/create/", views.create_exma, name="create_exam"),
    path("exam/delete/", views.delete_exam, name="delete_exam"),
    path("exam/edit/", views.edit_exam, name="edit_exam"),
    path("exam/show/", views.show_exam, name="show_exam"),
    path("exam/all/", views.show_all_exams, name="show_all_exams"),

    # Question
    path("question/create/", views.create_question, name="create_question"),
    path("question/delete/", views.delete_question, name="delete_question"),
    path("question/show/", views.show_question, name="show_question"),

    # Option
    path("option/create/", views.create_option, name="create_option"),
    path("option/delete/", views.delete_option, name="delete_option"),

    # Exam Result
    path("exam-result/create/", views.create_exam_result, name="create_exam_result"),

    # Answers
    path("answer/create/", views.create_answer, name="create_answer"),
]
