from django.contrib import admin
from django.urls import path, include

# ============================================
# Project URL Configuration
# Base domain: /
# ============================================

urlpatterns = [

    # -------------------------------------------------
    # Authentication System Endpoints
    # Base URL prefix: /auth/
    # Handles:
    #   - Signin (register)
    #   - Manual login
    #   - JWT login
    # -------------------------------------------------
    path("auth/", include("AuthenticationSystem.urls")),


    # -------------------------------------------------
    # Core Exam System Endpoints
    # Base URL prefix: /core/
    # Handles:
    #   - Exams
    #   - Questions
    #   - Options
    #   - Exam Results
    #   - Answers
    # -------------------------------------------------
    path("core/", include("Core.urls")),


    # -------------------------------------------------
    # Admin Panel (optional)
    # Enable if needed:
    # path("admin/", admin.site.urls)
    # -------------------------------------------------
]
