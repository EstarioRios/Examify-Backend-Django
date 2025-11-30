# 🧾 Exam System Django

## 📘 Overview

This backend provides a complete **exam management system** with **user authentication** through RESTful API endpoints.  
Built using **Django** and **Django REST Framework (DRF)** with **JWT authentication** for secure access.

The system allows users to:

- Register and log in (with or without JWT)
- Create, edit, delete exams
- Create, edit, delete questions and options
- Start an exam (creates an ExamResult)
- Submit answers for questions
- Enforce ownership and permission checks (creator-only actions)
- Receive consistent HTTP responses and error codes

Base URL structure:

- `/auth/` → Authentication (signup/login)
- `/core/` → Exam system (exams, questions, options, results, answers)

---

## 🔐 Authentication Endpoints (`/auth/`)

| Endpoint | Method | Auth Required | Description |
|----------|-------|---------------|-------------|
| `/auth/singin/` | POST | ❌ | User registration (signup) |
| `/auth/manual-login/` | POST | ❌ | Manual login (optional JWT tokens) |
| `/auth/login/` | POST | ✅ | Validate JWT login |

### 1️⃣ Signup – Create New User

**POST** `/auth/singin/`  

**Request Body (JSON):**

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "user_name": "john_doe",
  "user_type": "student",
  "password": "your_password"
}
```

**Success Response (`201 Created`):**

```json
{
  "msg": "user created",
  "user": {
    "first_name": "John",
    "last_name": "Doe",
    "user_name": "john_doe",
    "user_type": "student"
  },
  "tokens": {
    "access": "ACCESS_TOKEN",
    "refresh": "REFRESH_TOKEN"
  }
}
```

**Error Responses:**

- `400 Bad Request` → missing required fields  
- `403 Forbidden` → username already exists  

---

### 2️⃣ Manual Login – Username + Password

**POST** `/auth/manual-login/`  

**Request Body (JSON):**

```json
{
  "id_code": "john_doe",
  "password": "your_password",
  "remember": true
}
```

**Behavior:**

- If `remember=true` → returns **JWT tokens + user info**  
- If `remember=false` → returns **user info only**  

**Success Response (remember=true):**

```json
{
  "success": "Login successful",
  "tokens": {
    "access": "ACCESS_TOKEN",
    "refresh": "REFRESH_TOKEN"
  },
  "user": {
    "first_name": "John",
    "last_name": "Doe",
    "user_name": "john_doe",
    "user_type": "student"
  }
}
```

**Error Response:**  

- `404 Not Found` → Invalid credentials  

---

### 3️⃣ JWT Login – Preferred Method

**POST** `/auth/login/`  

**Headers:**

```
Authorization: Bearer ACCESS_TOKEN
```

**Behavior:**

- Validates JWT token from request headers  
- Returns user dashboard info if valid  

**Success Response:**

```json
{
  "success": "Login successful",
  "user": {
    "first_name": "John",
    "last_name": "Doe",
    "user_name": "john_doe",
    "user_type": "student"
  }
}
```

**Error Response:**  

- `400 Bad Request` → Invalid or expired JWT  

---

## 🧾 Core Exam Endpoints (`/core/`)

All endpoints under `/core/` require JSON body for POST/PUT/DELETE and query params for GET requests.  
Authentication: JWT in `Authorization` header required for all except explicitly stated.

| Section | Endpoint | Method | Auth | Description |
|---------|----------|--------|------|-------------|
| Exam | `/core/exam/create/` | POST | ✅ | Create new exam |
| Exam | `/core/exam/delete/` | DELETE | ✅ | Delete exam |
| Exam | `/core/exam/edit/` | PUT | ✅ | Edit exam |
| Exam | `/core/exam/show/` | GET | ✅ | Show exam by id |
| Exam | `/core/exam/all/` | GET | ✅ | List all exams |
| Question | `/core/question/create/` | POST | ✅ | Create new question |
| Question | `/core/question/delete/` | DELETE | ✅ | Delete question |
| Question | `/core/question/show/` | GET | ✅ | Show question by id |
| Option | `/core/option/create/` | POST | ✅ | Create new option |
| Option | `/core/option/delete/` | DELETE | ✅ | Delete option |
| ExamResult | `/core/exam-result/create/` | POST | ✅ | Start exam (create exam result) |
| Answer | `/core/answer/create/` | POST | ✅ | Submit answer |

---

### EXAM Endpoints

#### 1️⃣ Create Exam

**POST** `/core/exam/create/`  

**Request Body:**

```json
{
  "title": "Algebra Basics",
  "description": "Basic algebra test"
}
```

**Success Response (`201 Created`):**

```json
{
  "id": 1,
  "title": "Algebra Basics",
  "description": "Basic algebra test",
  "creator": "teacher_user"
}
```

**Error Responses:**  

- `400 Bad Request` → missing title/description  
- `403 Forbidden` → non-teacher trying to create exam  

---

#### 2️⃣ Delete Exam

**DELETE** `/core/exam/delete/`  

**Request Body:**

```json
{
  "id": 1
}
```

**Success Response (`204 No Content`)**  

**Error Responses:**  

- `404 Not Found` → exam doesn't exist  
- `403 Forbidden` → user not creator  

---

#### 3️⃣ Edit Exam

**PUT** `/core/exam/edit/`  

**Request Body:**

```json
{
  "id": 1,
  "new_title": "Updated Algebra",
  "new_description": "Updated description"
}
```

**Success Response (`200 OK`):**

```json
{
  "id": 1,
  "title": "Updated Algebra",
  "description": "Updated description",
  "creator": "teacher_user"
}
```

---

#### 4️⃣ Show Exam

**GET** `/core/exam/show/?id=1`  

**Success Response (`200 OK`):**

```json
{
  "id": 1,
  "title": "Algebra Basics",
  "description": "Basic algebra test",
  "creator": "teacher_user"
}
```

---

#### 5️⃣ Show All Exams

**GET** `/core/exam/all/`  

**Success Response (`200 OK`):**

```json
[
  {
    "id": 1,
    "title": "Algebra Basics",
    "description": "Basic algebra test",
    "creator": "teacher_user"
  },
  {
    "id": 2,
    "title": "Geometry",
    "description": "Geometry test",
    "creator": "teacher_user"
  }
]
```

---

### QUESTION Endpoints

#### Create Question

**POST** `/core/question/create/`  

**Request Body:**

```json
{
  "exam_id": 1,
  "question_content": "What is 2 + 2?",
  "question_score": 5
}
```

**Success Response (`201 Created`):**

```json
{
  "id": 1,
  "exam_id": 1,
  "content": "What is 2 + 2?",
  "score": 5
}
```

---

#### Delete Question

**DELETE** `/core/question/delete/`  

**Request Body:**

```json
{
  "id": 1
}
```

**Success Response:** `204 No Content`  

---

#### Show Question

**GET** `/core/question/show/?id=1`  

**Success Response (`200 OK`):**

```json
{
  "id": 1,
  "exam_id": 1,
  "content": "What is 2 + 2?",
  "score": 5,
  "options": [
    {"id": 1, "content": "4", "is_correct": true},
    {"id": 2, "content": "3", "is_correct": false}
  ]
}
```

---

### OPTION Endpoints

#### Create Option

**POST** `/core/option/create/`  

**Request Body:**

```json
{
  "question_id": 1,
  "content": "4",
  "is_correct": true
}
```

**Success Response (`201 Created`):**

```json
{
  "id": 1,
  "question_id": 1,
  "content": "4",
  "is_correct": true
}
```

---

#### Delete Option

**DELETE** `/core/option/delete/`  

**Request Body:**

```json
{
  "id": 1
}
```

**Success Response:** `204 No Content`  

---

### EXAM RESULT Endpoints

#### Create Exam Result (Start Exam)

**POST** `/core/exam-result/create/`  

**Request Body:**

```json
{
  "exam_id": 1
}
```

**Success Response (`201 Created`):**

```json
{
  "id": 1,
  "exam_id": 1,
  "student": "student_user",
  "start_time": "2025-11-30T22:00:00Z"
}
```

---

### ANSWER Endpoints

#### Create Answer

**POST** `/core/answer/create/`  

**Request Body:**

```json
{
  "exam_result_id": 1,
  "question_id": 1,
  "selected_option_id": 1
}
```

**Success Response (`201 Created`):**

```json
{
  "id": 1,
  "exam_result_id": 1,
  "question_id": 1,
  "selected_option_id": 1,
  "is_correct": true
}
```

---

## ⚙️ Tech Stack

- **Django** – backend framework  
- **Django REST Framework (DRF)** – API serialization & view handling  
- **JWT Authentication** – `djangorestframework-simplejwt`  
- **SQLite / PostgreSQL** – supported databases  
- **Python 3.10+**  

---

## 🚀 Quick Start

```bash
# Clone repo
git clone https://github.com/EstarioRios/Examify-Backend-Django.git
cd Examify-Backend-Django

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start dev server
python manage.py runserver
```

---

✍️ **Author:** Abolfazl Khezri  
🌐 GitHub: <https://github.com/EstarioRios>  
📸 Instagram: @estariorios
