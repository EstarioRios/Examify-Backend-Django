from django.urls import path
from . import views

# ============================================
# Core API Endpoints
# Base URL prefix: /core/
# ============================================

urlpatterns = [

    # ============================================
    #                    EXAM
    # ============================================

    # -------------------------------------------------
    # CREATE EXAM
    # Endpoint: POST /core/exam/create/
    # Description:
    #   - Creates a new exam owned by the authenticated user (creator)
    #   - Required fields: exam_title, exam_description
    #   - Returns: Created exam data
    #   - Authentication: Required (JWT)
    # -------------------------------------------------
    path("exam/create/", views.create_exma, name="create_exam"),

    # -------------------------------------------------
    # DELETE EXAM
    # Endpoint: DELETE /core/exam/delete/
    # Description:
    #   - Deletes an exam by exam_id
    #   - Only the creator of the exam can delete it
    #   - Required fields: id
    #   - Authentication: Required (JWT)
    # -------------------------------------------------
    path("exam/delete/", views.delete_exam, name="delete_exam"),

    # -------------------------------------------------
    # EDIT EXAM
    # Endpoint: PUT /core/exam/edit/
    # Description:
    #   - Edits exam title/description
    #   - Only the creator can edit
    #   - Required fields: id, (new_title | new_description)
    #   - Authentication: Required (JWT)
    # -------------------------------------------------
    path("exam/edit/", views.edit_exam, name="edit_exam"),

    # -------------------------------------------------
    # SHOW EXAM
    # Endpoint: GET /core/exam/show/?id=<exam_id>
    # Description:
    #   - Returns details of a specific exam
    #   - Required query param: id
    #   - Authentication: Required (JWT)
    # -------------------------------------------------
    path("exam/show/", views.show_exam, name="show_exam"),

    # -------------------------------------------------
    # SHOW ALL EXAMS
    # Endpoint: GET /core/exam/all/
    # Description:
    #   - Returns a list of all exams created by the authenticated user
    #   - Authentication: Required (JWT)
    # -------------------------------------------------
    path("exam/all/", views.show_all_exams, name="show_all_exams"),


    # ============================================
    #                  QUESTION
    # ============================================

    # -------------------------------------------------
    # CREATE QUESTION
    # Endpoint: POST /core/question/create/
    # Description:
    #   - Adds a new question to a specific exam
    #   - Only the exam creator can add questions
    #   - Required fields: exam_id, question_title, question_score
    #   - Authentication: Required (JWT)
    # -------------------------------------------------
    path("question/create/", views.create_question, name="create_question"),

    # -------------------------------------------------
    # DELETE QUESTION
    # Endpoint: DELETE /core/question/delete/
    # Description:
    #   - Deletes a question by question_id
    #   - Only exam creator can delete
    #   - Required fields: id
    #   - Authentication: Required (JWT)
    # -------------------------------------------------
    path("question/delete/", views.delete_question, name="delete_question"),

    # -------------------------------------------------
    # SHOW QUESTION
    # Endpoint: GET /core/question/show/?id=<question_id>
    # Description:
    #   - Returns the question and all its options
    #   - Required query param: id
    #   - Authentication: Required (JWT)
    # -------------------------------------------------
    path("question/show/", views.show_question, name="show_question"),


    # ============================================
    #                   OPTION
    # ============================================

    # -------------------------------------------------
    # CREATE OPTION
    # Endpoint: POST /core/option/create/
    # Description:
    #   - Adds an answer option to a specific question
    #   - Only the exam creator can add options
    #   - Required fields: question_id, option_title, is_correct
    #   - Authentication: Required (JWT)
    # -------------------------------------------------
    path("option/create/", views.create_option, name="create_option"),

    # -------------------------------------------------
    # DELETE OPTION
    # Endpoint: DELETE /core/option/delete/
    # Description:
    #   - Deletes a specific option
    #   - Only exam creator can delete
    #   - Required fields: id
    #   - Authentication: Required (JWT)
    # -------------------------------------------------
    path("option/delete/", views.delete_option, name="delete_option"),


    # ============================================
    #                EXAM RESULT
    # ============================================

    # -------------------------------------------------
    # CREATE EXAM RESULT (Start Exam)
    # Endpoint: POST /core/exam-result/create/
    # Description:
    #   - Creates an ExamResult object for a student starting an exam
    #   - Required fields: exam_id
    #   - Authentication: Required (JWT)
    # -------------------------------------------------
    path("exam-result/create/", views.create_exam_result, name="create_exam_result"),


    # ============================================
    #                 ANSWERS
    # ============================================

    # -------------------------------------------------
    # CREATE ANSWER
    # Endpoint: POST /core/answer/create/
    # Description:
    #   - Saves the student's selected option for a question
    #   - Required fields: exam_result_id, question_id, selected_option_id
    #   - Ensures:
    #       * option belongs to the question
    #       * exam_result belongs to the user
    #   - Authentication: Required (JWT)
    # -------------------------------------------------
    path("answer/create/", views.create_answer, name="create_answer"),
]
