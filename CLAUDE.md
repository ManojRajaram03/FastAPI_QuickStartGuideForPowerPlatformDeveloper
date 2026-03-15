# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Test-Driven Development (TDD)** project for building a FastAPI Contact Book API. The test suite (`test_main.py`) is already complete with 28 tests covering all functionality. The implementation (`main.py`) should be built iteratively to make these tests pass.

## Development Commands

### Install Dependencies
```bash
pip install fastapi uvicorn pytest httpx
```

### Run All Tests
```bash
pytest test_main.py -v
```

### Run Tests with Short Traceback (recommended during development)
```bash
pytest test_main.py -v --tb=short
```

### Run Specific Test Class
```bash
pytest test_main.py::TestCreateContact -v
pytest test_main.py::TestListContacts -v
pytest test_main.py::TestSearchContacts -v
pytest test_main.py::TestGetContact -v
pytest test_main.py::TestUpdateContact -v
pytest test_main.py::TestDeleteContact -v
pytest test_main.py::TestEdgeCases -v
```

### Run Single Test
```bash
pytest test_main.py::TestCreateContact::test_create_contact_returns_201 -v
```

### Run Backend Server
```bash
uvicorn main:app --reload
```

### Serve Frontend (after index.html is created)
```bash
python -m http.server 5500
```

## Architecture

### TDD Workflow
This project follows strict **RED → GREEN → REFACTOR** methodology:
1. **RED** - Run tests first, verify they fail (proves tests work)
2. **GREEN** - Write minimum code to make tests pass
3. **REFACTOR** - Clean up code while keeping tests green

### API Structure
The Contact Book API is built around a single resource (contacts) with full CRUD operations:

- **POST /contacts** - Create new contact (returns 201)
- **GET /contacts** - List all contacts with optional search via `?q=` query parameter
- **GET /contacts/{id}** - Retrieve single contact by ID (returns 404 if not found)
- **PUT /contacts/{id}** - Update existing contact with partial updates (returns 404 if not found)
- **DELETE /contacts/{id}** - Delete contact (returns 404 if not found)

### Data Models
Three Pydantic models are needed:

1. **ContactCreate** - For POST requests
   - `name`: required, must be non-empty and non-whitespace string
   - `email`: optional
   - `phone`: optional
   - `notes`: optional

2. **ContactResponse** - For all responses
   - All fields from ContactCreate plus:
   - `id`: server-generated unique identifier (string)

3. **ContactUpdate** - For PUT requests
   - ALL fields optional (including name)
   - Enables partial updates while preserving unmodified fields

### Data Storage
- In-memory list/dictionary for storing contacts
- **Critical requirement**: Test isolation - the store must reset between tests
- Implementation approaches:
  - Use a pytest fixture with `autouse=True` that clears the store
  - Use FastAPI dependency injection with `TestClient` overrides
  - Implement a reset endpoint (less ideal)

### Search Functionality
The `?q=` query parameter on GET /contacts must:
- Search across ALL fields: name, email, phone, notes
- Be case-insensitive
- Return empty list (not error) when no matches found
- Return all contacts when query is empty or omitted

### CORS Configuration
Must support browser-based frontend:
- Allow all origins (for development)
- Allow all methods
- Allow all headers
- Use `fastapi.middleware.cors.CORSMiddleware`

## Implementation Order

The TDD_GUIDE.md specifies the exact incremental implementation order:

1. **Step 1**: Pydantic models + POST /contacts (6 tests in TestCreateContact)
2. **Step 2**: GET /contacts + test isolation (2 tests in TestListContacts + 1 isolation test)
3. **Step 3**: Search with ?q= parameter (6 tests in TestSearchContacts)
4. **Step 4**: GET /contacts/{id} (2 tests in TestGetContact)
5. **Step 5**: PUT /contacts/{id} with partial updates (4 tests in TestUpdateContact)
6. **Step 6**: DELETE /contacts/{id} (4 tests in TestDeleteContact)
7. **Step 7**: Edge case validation + CORS (3 tests in TestEdgeCases)
8. **Step 8**: Frontend (index.html with vanilla JS)

**Always verify tests pass after each step before proceeding.**

## Key Implementation Details

### ID Generation
- Contact IDs must be unique strings
- Suggested approach: `str(uuid.uuid4())` or similar

### Validation Edge Cases
- Empty string name ("") must return 422
- Whitespace-only name ("   ") must return 422
- Missing name field must return 422
- These validations should be in the Pydantic model using constraints

### Partial Updates (PUT)
The PUT endpoint must:
- Accept request body where all fields are optional
- Only update fields that are present in the request
- Preserve existing values for fields not included in request
- Use `.model_dump(exclude_unset=True)` pattern with Pydantic

### Error Handling
- Return 404 with meaningful detail message for non-existent resources
- Use FastAPI's `HTTPException` for error responses

### Frontend Requirements
When building index.html:
- Single-file application (HTML + CSS + JS in one file)
- Use vanilla JavaScript (no frameworks)
- All API calls target `http://localhost:8000`
- Features: create, search (real-time), edit, delete with confirmation
- Use `fetch()` API for all HTTP requests

## Testing Notes

- All 28 tests must pass before the backend is considered complete
- Tests use `fastapi.testclient.TestClient` - no actual server needed for testing
- The test file provides fixtures: `client`, `sample_contact`, `another_contact`
- Helper function `create_contact()` is available in tests for convenience
- Test isolation is critical - each test should start with empty contact list

## FastAPI Auto-Documentation

Once the server is running, interactive API docs are available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
