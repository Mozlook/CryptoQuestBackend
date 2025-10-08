# CryptoQuest Backend (Django + PostgreSQL)

Backend service for **CryptoQuest** — a web app for solving coding puzzles (“zagadki”).  
This README documents the **actual endpoints** present in `zagadki/api/urls.py` and their behavior from `zagadki/api/views.py`.

**Stack:** Django (+ Django REST Framework), PostgreSQL, custom `User` model with a `progress` field.

> If you include this app with `path("api/", include("zagadki.api.urls"))` in your project `urls.py`, then the effective base path will be `/api/` (examples below assume that).

---

## Quickstart

```bash
git clone https://github.com/Mozlook/CryptoQuestBackend.git
cd CryptoQuestBackend

python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Create DB & run migrations
python manage.py migrate
python manage.py runserver
```

Environment (example `.env`):

```dotenv
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Prefer DATABASE_URL or set individual DB_* values
DATABASE_URL=postgres://user:password@localhost:5432/cryptoquest

# CORS (frontend dev origin)
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

---

## Authentication & CSRF model (as implemented)

- **Token login**: `POST /api/login/` returns a DRF token (string) for the user; include it in subsequent requests as:  
  `Authorization: Token <your-token>`
- **Protected view**: `GET /api/sprawdz-progres/` requires authentication (`IsAuthenticated`) and returns the current user’s progress.
- **Optional auth**: `POST /api/sprawdz-odpowiedz/` accepts requests from anonymous users **or** token-authenticated users.
  - If **authenticated**, the backend checks the puzzle number matching `user.progress`.
  - If **anonymous**, it assumes puzzle number `1`.
- **CSRF**: `GET /api/get-csrf/` issues a CSRF token and sets the `csrftoken` cookie with attributes: `Secure=True`, `HttpOnly=False`, `SameSite=None`.

> Note: Because `Secure=True`, browsers only send that cookie over **HTTPS**. For local HTTP testing, use token auth (no CSRF) or terminate TLS locally.

---

## API Reference

> Base URL assumed to be `/api/`. If you mount the app differently, adjust paths accordingly.

### 1) Errors / Reports — `POST /api/bledy/`

- **Purpose**: Accepts error/feedback payload via **multipart/form-data** or **form-data**.
- **Parsers**: `MultiPartParser`, `FormParser`.
- **Serializer**: `BledySerializer` (fields depend on serializer definition).
- **Auth**: not explicitly enforced in view (falls back to project defaults).

**Request (multipart/form-data)** — example keys (adjust to your serializer):

```
description=...
screenshot=<file>
```

**Responses**:

- **201** — on success, returns serialized object.
- **400** — validation errors.

### 2) CSRF token — `GET /api/get-csrf/`

Returns a JSON body and sets a **`csrftoken`** cookie.

**Response 200 (JSON)**:

```json
{
  "detail": "CSRF token generated",
  "csrftoken": "<token-value>"
}
```

**Cookie attributes set by the view**:

- Name: `csrftoken`
- `Secure=True`, `HttpOnly=False`, `SameSite=None`, `Max-Age=3600`

### 3) Registration — `POST /api/register/`

Registers a new user using `RegistrationSerializer`.

**Request (JSON)**:

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "StrongPassword123!"
}
```

**Responses**:

- **201**:
  ```json
  {
    "message": "User created successfully",
    "email": "alice@example.com",
    "username": "alice"
  }
  ```
- **400**:
  ```json
  { "errors": { "<field>": ["<message>", "..."] } }
  ```
- **500**:
  ```json
  { "error": "<exception message>" }
  ```

### 4) Login (Token) — `POST /api/login/`

Authenticates a user and returns a **DRF Token**.

**Request (JSON)**:

```json
{
  "username": "alice",
  "password": "StrongPassword123!",
  "progress": 2 // optional: if < 3 and current user.progress == 1, it bumps progress
}
```

**Response 200**:

```json
{ "token": "<token-string>" }
```

**Response 400**:

```json
{ "error": "Invalid credentials" }
```

**Special behavior**:

- If `progress` is provided, **is integer**, `< 3`, and the authenticated user’s `progress == 1`, the backend updates the user’s progress to that value. Otherwise it ignores the provided progress.

### 5) Check progress — `GET /api/sprawdz-progres/` (auth required)

- **Permissions**: `IsAuthenticated`
- **Response 200**:
  ```json
  { "progress": <int> }
  ```

### 6) Check answer — `POST /api/sprawdz-odpowiedz/` (auth optional)

- **Authentication**: `TokenAuthentication` declared, but `AllowAny` permissions — so both anonymous and authenticated requests are accepted.
- **Behavior**:
  - Determines the puzzle number as `user.progress` (if authenticated) or `1` (if anonymous).
  - Fetches `Zagadki` by `numer` (puzzle number).
  - Compares `request.data["answer"]` (case/whitespace-insensitive) to `zagadka.kod`.
  - If correct:
    - For **authenticated** users: increments `user.progress` by 1 and returns `{"answer": true}`.
    - For **anonymous** users: returns `{"answer": true, "progress": 2}` (no persisted state).
  - If incorrect: returns `{"answer": false}`.

**Requests**:

```json
{ "answer": "..." }
```

**Responses**:

- **200** (correct, authenticated):
  ```json
  { "answer": true }
  ```
- **200** (correct, anonymous):
  ```json
  { "answer": true, "progress": 2 }
  ```
- **200** (incorrect):
  ```json
  { "answer": false }
  ```
- **400** (missing answer):
  ```json
  { "error": "Brak odpowiedzi" }
  ```
- **404** (puzzle not found for computed number):
  ```json
  { "error": "Nie znaleziono zagadki" }
  ```

---

## cURL Examples

> Adjust base URL/token as needed.

**Register**

```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"StrongPassword123!"}'
```

**Login (get token)**

```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"StrongPassword123!"}'
```

**Check progress (requires token)**

```bash
curl -X GET http://127.0.0.1:8000/api/sprawdz-progres/ \
  -H "Authorization: Token <your-token>"
```

**Check answer (optional token)**

```bash
curl -X POST http://127.0.0.1:8000/api/sprawdz-odpowiedz/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <your-token>" \
  -d '{"answer":"..."}'
```

**Send report / error (multipart form-data)**

```bash
curl -X POST http://127.0.0.1:8000/api/bledy/ \
  -H "Authorization: Token <your-token>" \
  -F "description=Something went wrong" \
  -F "screenshot=@/path/to/file.png"
```

---

## Notes & Recommendations

- **Token header**: for protected endpoints, send `Authorization: Token <token>`.
- **Anonymous flow**: `sprawdz-odpowiedz` works without auth, but persistent progress only updates for authenticated users.
- **CSRF**: If you plan to use session-based auth or `fetch`/AJAX with cookies, hit `/api/get-csrf/` first to obtain the cookie and include the token header per Django’s CSRF rules on modifying requests.
- **Model expectations**: `Zagadki` model exposes at least `numer` (int) and `kod` (string) used here.
- **Progress semantics**: `progress` is assumed to be a 1-based puzzle index; correct answers advance it by 1.

---

## License

MIT © Mozlook
