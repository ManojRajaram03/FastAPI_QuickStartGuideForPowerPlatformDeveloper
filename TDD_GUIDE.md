# Contact Book API — TDD Guide with Claude Code

## 📁 Project Setup

Create a project folder and place `test_main.py` in it:

```
contact-book/
├── test_main.py    ← (the test file you already have)
├── main.py         ← (you'll build this)
└── index.html      ← (frontend, built last)
```

Install dependencies:

```bash
pip install fastapi uvicorn pytest httpx
```

---

## 🔴🟢🔁 The TDD Cycle

The rhythm is always: **RED → GREEN → REFACTOR**

1. **RED** — Run tests, watch them fail (proves tests are real)
2. **GREEN** — Write the minimum code to pass
3. **REFACTOR** — Clean up without breaking tests

Run tests anytime with:

```bash
pytest test_main.py -v --tb=short
```

---

## Step-by-Step Execution Plan

### Step 0: Verify Tests Fail (RED)

Before writing any code, create an empty `main.py` and confirm everything fails:

```bash
# Create a minimal main.py so the import doesn't crash
echo 'from fastapi import FastAPI; app = FastAPI()' > main.py
pytest test_main.py -v --tb=short
```

You should see **all 28 tests failing**. Good — that's the RED phase.

---

### Step 1: Pydantic Models + Create Endpoint

**What you're building:** The data models and POST /contacts

**Claude Code prompt:**

```
Look at test_main.py in this project. I'm doing TDD — all tests are written.

For Step 1, make ONLY these test classes pass:
- TestCreateContact (all 6 tests)

Build in main.py:
1. A Pydantic model "ContactCreate" for the request body (name required, email/phone/notes optional). Name must be a non-empty, non-whitespace string.
2. A Pydantic model "ContactResponse" that adds an "id" field
3. An in-memory list to store contacts
4. POST /contacts endpoint that returns 201

Don't implement any other endpoints yet. Keep it minimal.
```

**Verify:** `pytest test_main.py::TestCreateContact -v` → all 6 green

---

### Step 2: List Contacts Endpoint

**What you're building:** GET /contacts (list all)

**Claude Code prompt:**

```
Next TDD step. Make TestListContacts pass (2 tests).

Add GET /contacts that returns the full list from the in-memory store.
Return an empty list if no contacts exist.

IMPORTANT: We need test isolation — contacts created in one test
should not leak into another. Add a fixture or mechanism to reset
the in-memory store between tests. Look at test "test_contacts_are_isolated_between_tests"
for what's expected.
```

**Verify:** `pytest test_main.py::TestListContacts test_main.py::TestEdgeCases::test_contacts_are_isolated_between_tests -v`

---

### Step 3: Search Contacts

**What you're building:** Query parameter `?q=` on GET /contacts

**Claude Code prompt:**

```
Next TDD step. Make TestSearchContacts pass (all 6 tests).

Modify GET /contacts to accept an optional query parameter "q".
When provided, filter contacts where the query matches (case-insensitive)
against name, email, phone, or notes fields.
When q is empty or not provided, return all contacts.
```

**Verify:** `pytest test_main.py::TestSearchContacts -v` → all 6 green

---

### Step 4: Get Single Contact

**What you're building:** GET /contacts/{id}

**Claude Code prompt:**

```
Next TDD step. Make TestGetContact pass (2 tests).

Add GET /contacts/{id} that:
- Returns the contact with matching id (200)
- Returns 404 with a detail message if id not found
```

**Verify:** `pytest test_main.py::TestGetContact -v` → all 2 green

---

### Step 5: Update Contact

**What you're building:** PUT /contacts/{id}

**Claude Code prompt:**

```
Next TDD step. Make TestUpdateContact pass (all 4 tests).

Add PUT /contacts/{id} that:
- Accepts a JSON body where ALL fields are optional
- Updates ONLY the fields provided (partial update)
- Preserves fields that were not included in the request
- Returns the updated contact (200)
- Returns 404 if the id doesn't exist

Create a separate Pydantic model "ContactUpdate" where all fields
including name are Optional.
```

**Verify:** `pytest test_main.py::TestUpdateContact -v` → all 4 green

---

### Step 6: Delete Contact

**What you're building:** DELETE /contacts/{id}

**Claude Code prompt:**

```
Next TDD step. Make TestDeleteContact pass (all 4 tests).

Add DELETE /contacts/{id} that:
- Removes the contact from the store
- Returns {"message": "Contact deleted"} with status 200
- Returns 404 if the id doesn't exist
```

**Verify:** `pytest test_main.py::TestDeleteContact -v` → all 4 green

---

### Step 7: Edge Cases + CORS

**What you're building:** Validation polish and CORS middleware

**Claude Code prompt:**

```
Next TDD step. Make TestEdgeCases pass (all 3 tests).

Then add CORS middleware to the app so a browser-based frontend
on any origin can call the API. Allow all origins, methods, and headers.

Also verify ALL 28 tests pass: pytest test_main.py -v
```

**Verify:** `pytest test_main.py -v` → **ALL 28 GREEN** ✅

---

### Step 8: Frontend

**What you're building:** A single index.html that talks to the API

**Claude Code prompt:**

```
All 28 backend tests pass. Now build a frontend.

Create index.html — a single-file frontend (HTML + CSS + JS) for the
Contact Book API running at http://localhost:8000.

Features:
- A form to add new contacts (name, email, phone, notes)
- A search bar that filters in real-time via GET /contacts?q=
- Contact cards showing each contact's details
- Edit button on each card that populates the form for updating
- Delete button with confirmation
- All API calls use fetch() to http://localhost:8000

Keep the UI clean and simple. Use vanilla JS, no frameworks.
```

---

## 🚀 Running the Full App

Terminal 1 — start the backend:

```bash
uvicorn main:app --reload
```

Terminal 2 — serve the frontend:

```bash
python -m http.server 5500
```

Then open http://localhost:5500 in your browser.

Visit http://localhost:8000/docs for FastAPI's auto-generated Swagger UI.

---

## 🧠 Key Concepts You'll Learn Along the Way

| Step | Concept |
|------|---------|
| 1 | Pydantic models, request validation, status codes |
| 2 | GET endpoints, returning lists, test isolation |
| 3 | Query parameters, filtering, case-insensitive search |
| 4 | Path parameters, 404 error handling |
| 5 | Partial updates, PUT vs PATCH semantics |
| 6 | DELETE operations, confirming side effects |
| 7 | CORS middleware, input validation edge cases |
| 8 | fetch() API, frontend-backend communication |

---

## 💡 Tips

- **Run tests after every change** — that's the whole point of TDD
- **Read the test names** — they describe exactly what's expected
- **Check `pytest --tb=long`** if a failure message is unclear
- **Use `http://localhost:8000/docs`** — FastAPI gives you free Swagger docs
- After all tests pass, try breaking things intentionally to see what the tests catch
