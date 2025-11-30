
# 🧾 Exam System Django – README

## 📘 Overview

This backend provides **user authentication** and a complete **exam management system** through RESTful API endpoints.  
It is built using **Django** and **Django REST Framework (DRF)** with **JWT authentication** for secure access.

The system allows users to:

- Register and log in (with or without JWT tokens)
- Create, edit, and delete exams
- Create, edit, and delete questions and options
- Start an exam (creates an ExamResult)
- Submit answers for questions
- Enforce ownership and permission checks (creator-only actions)
- Receive clear, consistent HTTP responses and error codes

---

## 🔐 Authentication Endpoints (`/auth/`)

### 1️⃣ Signup – Create New User

**POST** `/auth/singin/`

**Body (JSON):**

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "user_name": "john_doe",
  "user_type": "author",
  "password": "your_password"
}
```

**Auth:** None (AllowAny)  
**Success Response:** `201 Created`

```json
{
  "msg": "user created",
  "user": { ... },
  "tokens": {
    "access": "ACCESS_TOKEN",
    "refresh": "REFRESH_TOKEN"
  }
}
```

**Error Responses:**

- `400 Bad Request` → Missing required fields  
- `403 Forbidden` → Username already exists  

---

### 2️⃣ Manual Login – Username + Password

**POST** `/auth/manual-login/`

**Body (JSON):**

```json
{
  "id_code": "john_doe",
  "password": "your_password",
  "remember": true
}
```

**Behavior:**

- If `remember = true` → returns **JWT tokens (access & refresh)** plus user data
- If `remember = false` → returns user data only (no tokens)

**Success Response (remember = true):**

```json
{
  "success": "Login successful",
  "tokens": {
    "access": "ACCESS_TOKEN",
    "refresh": "REFRESH_TOKEN"
  },
  "user": { ... }
}
```

**Error Response:**  
`404 Not Found` → Invalid credentials  

---

### 3️⃣ Login via JWT – Preferred Method

**POST** `/auth/login/`

**Headers:**

```
Authorization: Bearer ACCESS_TOKEN
```

**Auth:** Token is validated manually inside the view.  
**Success Response:**

```json
{
  "success": "Login successful",
  "user": { ... }
}
```

**Error Response:**  
`400 Bad Request` → Invalid or expired JWT  

---

## 🧾 Core Exam Endpoints (`/core/`)

All endpoints under `/core/` expect JSON bodies for POST/PUT/DELETE requests and query params for GET requests (for example: `?id=123`).  
Authorization: Unless explicitly stated otherwise, endpoints under `/core/` require a valid JWT token in the `Authorization` header.

---

### EXAM Endpoints

#### 1️⃣ Create Exam

**POST** `/core/exam/create/`

**Headers:**

```
Authorization: Bearer ACCESS_TOKEN
```

**Body (JSON):**

```json
{
  "title": "Algebra Basics",
  "description": "A basic algebra test for beginners"
}
```

**Behavior:**

- Creates an `Exam` with the authenticated user as `creator`.
- Only allowed for users with `user_type == "teacher"`.

**Success Response:** `201 Created`  
**Error Responses:**

- `400 Bad Request` → missing fields or duplicate title  
- `403 Forbidden` → user is not a teacher

---

#### 2️⃣ Delete Exam

**DELETE** `/core/exam/delete/`

**Headers:**

```
Authorization: Bearer ACCESS_TOKEN
```

**Body (JSON):**

```json
{
  "id": 3
}
```

**Behavior:**

- Deletes the specified exam.
- Only the exam creator can delete their exam.

**Success Response:** `204 No Content`  
**Error Responses:**

- `400 Bad Request` → missing id  
- `404 Not Found` → exam doesn't exist  
- `403 Forbidden` → not the creator

---

#### 3️⃣ Edit Exam

**PUT** `/core/exam/edit/`

**Headers:**

```
Authorization: Bearer ACCESS_TOKEN
```

**Body (JSON):**

```json
{
  "id": 3,
  "new_title": "Updated Title",
  "new_description": "Updated description"
}
```

**Behavior:**

- Updates title and/or description of an exam.
- Only the creator can edit.

**Success Response:** `200 OK` with serialized exam.  
**Error Responses:** `400`, `403`, `404` as appropriate.

---

#### 4️⃣ Show Exam

**GET** `/core/exam/show/?id=<exam_id>`

**Behavior:**

- Returns the serialized `Exam` object for the provided `id`.

**Success Response:** `200 OK`  
**Error Responses:** `400`, `404`

---

#### 5️⃣ Show All Exams

**GET** `/core/exam/all/`

**Behavior:**

- Returns a list of all exams (serialized).
- Pagination is not implemented by default; consider adding if needed.

**Success Response:** `200 OK`

---

### QUESTION Endpoints

#### 1️⃣ Create Question

**POST** `/core/question/create/`

**Body (JSON):**

```json
{
  "exam_id": 1,
  "question_content": "What is 2 + 2?",
  "question_score": 5
}
```

**Behavior:**

- Adds a `Question` to the specified `Exam`.
- Only the exam creator can add questions.
- The `question_score` should be a numeric value (validated in the view).

**Success Response:** `201 Created`

---

#### 2️⃣ Delete Question

**DELETE** `/core/question/delete/`

**Body (JSON):**

```json
{
  "id": 10
}
```

**Behavior:** Only the exam creator can delete a question.  
**Success Response:** `204 No Content`

---

#### 3️⃣ Show Question

**GET** `/core/question/show/?id=<question_id>`

**Behavior:** Returns the question with its options serialized.  
**Success Response:** `200 OK`

---

### OPTION Endpoints

#### 1️⃣ Create Option

**POST** `/core/option/create/`

**Body (JSON):**

```json
{
  "id": 10,                 # question id
  "content": "4",
  "is_correct": true
}
```

**Behavior:**

- Adds an option (QOPtion) to a question.
- If `is_correct` is true, the view ensures there is no other `is_correct=True` option for that question.
- Only the exam creator may add options.

**Success Response:** `201 Created`  
**Error Responses:** `400`, `403`, `404`

---

#### 2️⃣ Delete Option

**DELETE** `/core/option/delete/`

**Body (JSON):**

```json
{
  "id": 22
}
```

**Behavior:** Only the exam creator may delete options.  
**Success Response:** `204 No Content`

---

### EXAM RESULT Endpoints

#### 1️⃣ Create Exam Result (Start Exam)

**POST** `/core/exam-result/create/`

**Body (JSON):**

```json
{
  "exam_id": 1
}
```

**Behavior:**

- Creates an `ExamResult` record with `start_time = now()` for the authenticated user.
- Returns `201 Created` and the created ExamResult id (if implemented).

---

### ANSWER Endpoints

#### 1️⃣ Create Answer

**POST** `/core/answer/create/`

**Body (JSON):**

```json
{
  "exam_result_id": 5,
  "question_id": 10,
  "selected_option_id": 22
}
```

**Behavior & Validation:**

- Validates that `ExamResult` exists and belongs to the authenticated user.
- Validates that `Question` and `QOPtion` exist.
- Validates that the `selected_option` belongs to the given `question`.
- Stores an `Answer` with `is_correct` computed from the selected option.

**Success Response:** `201 Created` with answer id and correctness flag.  
**Error Responses:** `400`, `403`, `404`

---

## ⚙️ Authentication Rules Summary

| Endpoint | Auth Required | Method | Description |
|---------|---------------|--------|-------------|
| `/auth/singin/` | ❌ | POST | User registration |
| `/auth/manual-login/` | ❌ | POST | Manual login (optional tokens) |
| `/auth/login/` | ✅ | POST | Token validation |
| `/core/exam/create/` | ✅ | POST | Create exam |
| `/core/exam/delete/` | ✅ | DELETE | Delete exam |
| `/core/exam/edit/` | ✅ | PUT | Edit exam |
| `/core/exam/show/` | ✅ | GET | Show exam |
| `/core/exam/all/` | ✅ | GET | List all exams |
| `/core/question/create/` | ✅ | POST | Add question |
| `/core/question/delete/` | ✅ | DELETE | Delete question |
| `/core/question/show/` | ✅ | GET | Show question |
| `/core/option/create/` | ✅ | POST | Add option |
| `/core/option/delete/` | ✅ | DELETE | Delete option |
| `/core/exam-result/create/` | ✅ | POST | Start exam |
| `/core/answer/create/` | ✅ | POST | Submit answer |

---

## 🧠 Tech Stack

- **Django** – Backend framework  
- **Django REST Framework (DRF)** – API serialization & view handling  
- **JWT Authentication** – Secure token-based authentication via `djangorestframework-simplejwt`  
- **SQLite / PostgreSQL** – Supported databases  
- **Python** 3.10+

---

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/yourusername/exam-system-backend.git
cd exam-system-backend

# 2. Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Start server (development)
python manage.py runserver
```

---

## 🧾 License

This project is licensed under the MIT License. Feel free to modify and distribute with attribution.

---

✍️ **Author:** Abolfazl Khezri  
🌐 GitHub: <https://github.com/EstarioRios>  
📸 Instagram: @estariorios
