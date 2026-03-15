# 🎓 Learning Guide - FastAPI for Power Platform Developers

This guide helps Power Platform developers understand FastAPI concepts by relating them to familiar Power Platform patterns.

---

## 📚 Table of Contents

1. [Core Concepts](#core-concepts)
2. [Power Platform Analogies](#power-platform-analogies)
3. [Understanding REST APIs](#understanding-rest-apis)
4. [Pydantic Models Explained](#pydantic-models-explained)
5. [HTTP Methods & Status Codes](#http-methods--status-codes)
6. [Hands-On Exercises](#hands-on-exercises)
7. [Common Patterns](#common-patterns)

---

## 🎯 Core Concepts

### What is FastAPI?

**FastAPI** is a modern Python web framework for building APIs.

**Power Platform Analogy:**
- **FastAPI** = Like creating Custom Connectors, but you control the entire backend
- **Endpoints** = Like Dataverse actions/functions
- **Pydantic Models** = Like Dataverse table schemas
- **Decorators (@app.get)** = Like "When HTTP request received" triggers

### What is an API?

**API** (Application Programming Interface) = A way for programs to talk to each other.

**Examples you already use:**
- Power Automate calling Dataverse
- Power Apps using Custom Connectors
- SharePoint REST API calls

This project teaches you to **BUILD** the API, not just consume it!

---

## 🔄 Power Platform Analogies

| FastAPI Concept | Power Platform Equivalent |
|----------------|---------------------------|
| `FastAPI()` | Creating a new app/flow |
| `@app.post()` | HTTP POST trigger in Power Automate |
| `@app.get()` | HTTP GET request action |
| Pydantic model | Dataverse table definition |
| `name: str` | Single line text column (required) |
| `email: Optional[str]` | Single line text column (optional) |
| `@field_validator` | Business rule in Dataverse |
| `HTTPException(404)` | Terminate action with error status |
| `response_model` | Parse JSON schema / Response action |
| Path parameter `{id}` | Dynamic content in URL |
| Query parameter `?q=` | URL query parameters |
| `contacts_db = []` | Collection variable in Power Apps |
| `.append()` | `Collect()` in Power Apps |
| `.pop()` | `Remove()` from collection |
| CORS middleware | API connection permissions |

---

## 🌐 Understanding REST APIs

### What is REST?

**REST** = Representational State Transfer (don't worry about the name!)

**Simple version:** A standard way to organize web APIs using:
- URLs (endpoints)
- HTTP methods (GET, POST, PUT, DELETE)
- JSON data

### REST Structure

```
Resource: /contacts
├── GET /contacts          → List all contacts
├── POST /contacts         → Create new contact
├── GET /contacts/{id}     → Get specific contact
├── PUT /contacts/{id}     → Update contact
└── DELETE /contacts/{id}  → Delete contact
```

**Power Platform Analogy:**
Like organizing Dataverse operations around a table:
- List Records
- Create Record
- Get Record
- Update Record
- Delete Record

### HTTP Methods (Verbs)

| Method | Purpose | Example | Dataverse Equivalent |
|--------|---------|---------|---------------------|
| GET | Read data | Get all contacts | List Records |
| POST | Create new | Create contact | Create Record |
| PUT | Update existing | Update contact | Update Record |
| DELETE | Remove | Delete contact | Delete Record |
| PATCH | Partial update | Update just email | Update Record (specific columns) |

---

## 📋 Pydantic Models Explained

### What are Pydantic Models?

**Definition:** Python classes that define data structure and validation rules.

**Power Platform Analogy:** Like creating a table in Dataverse with specific columns and data types.

### Example Comparison

**Dataverse Table:**
```
Table: Contact
├── Name (Single line text, Required)
├── Email (Single line text, Optional)
├── Phone (Single line text, Optional)
└── ID (Auto-generated GUID)
```

**Pydantic Model:**
```python
class Contact(BaseModel):
    name: str                    # Required
    email: Optional[str] = None  # Optional
    phone: Optional[str] = None  # Optional
    id: str                      # Required in response
```

### Why Use Models?

✅ **Automatic validation** - FastAPI checks data before your code runs
✅ **Auto-documentation** - API docs generated automatically
✅ **Type safety** - Catch errors before runtime
✅ **Clear structure** - Everyone knows what data looks like

**Power Platform Analogy:**
Like form validation in Power Apps - won't let user submit invalid data.

---

## 🔢 HTTP Status Codes

Every API response includes a status code telling you what happened.

### Common Status Codes

| Code | Name | Meaning | When Used |
|------|------|---------|-----------|
| **200** | OK | Success | GET, PUT, DELETE succeeded |
| **201** | Created | New resource created | POST succeeded |
| **400** | Bad Request | Invalid request | Malformed JSON |
| **404** | Not Found | Resource doesn't exist | ID not in database |
| **422** | Unprocessable Entity | Validation failed | Required field missing |
| **500** | Internal Server Error | Server crashed | Bug in code |

**Power Platform Analogy:**
Like error codes in Power Automate flows:
- Success (green check)
- Failed (red X)
- Skipped (gray)

### In This Project

- **201** - Contact created successfully
- **200** - Contact retrieved/updated/deleted
- **404** - Contact ID not found
- **422** - Name field empty or missing

---

## 🛠️ Hands-On Exercises

### Exercise 1: Create Your First Contact (API Docs)

1. Open http://localhost:8000/docs
2. Click on **POST /contacts**
3. Click **"Try it out"**
4. Enter JSON:
```json
{
  "name": "Your Name",
  "email": "your.email@example.com",
  "phone": "555-0123",
  "notes": "Learning FastAPI!"
}
```
5. Click **"Execute"**
6. See the response with auto-generated ID

**What happened?**
- FastAPI validated your JSON against `ContactCreate` model
- Generated a unique ID
- Stored in `contacts_db` list
- Returned `ContactResponse` with ID

---

### Exercise 2: Search Contacts

1. Create 2-3 contacts with different names
2. In API docs, try **GET /contacts**
3. Add query parameter: `q=John`
4. See filtered results

**What happened?**
- FastAPI parsed `?q=John` from URL
- Code looped through all contacts
- Compared (case-insensitive) against all fields
- Returned matching contacts only

---

### Exercise 3: Partial Update

1. Create a contact and note its ID
2. Try **PUT /contacts/{id}**
3. Send ONLY: `{"email": "newemail@test.com"}`
4. Get the contact back
5. Notice: Name and phone unchanged!

**What happened?**
- `model_dump(exclude_unset=True)` got only email field
- `.update()` merged email into existing contact
- Other fields preserved

---

### Exercise 4: Error Handling

1. Try **GET /contacts/fake-id-12345**
2. See 404 error response
3. Try **POST /contacts** with `{"email": "test@test.com"}` (no name)
4. See 422 validation error

**What happened?**
- 404: ID not in database → `HTTPException` raised
- 422: Name required → Pydantic validation failed automatically

---

## 🎨 Common Patterns

### Pattern 1: CRUD Operations

**CRUD** = Create, Read, Update, Delete

Every data-driven app needs these. In this project:

```python
# CREATE
@app.post("/contacts")
def create_contact(...)

# READ (all)
@app.get("/contacts")
def list_contacts(...)

# READ (one)
@app.get("/contacts/{id}")
def get_contact(...)

# UPDATE
@app.put("/contacts/{id}")
def update_contact(...)

# DELETE
@app.delete("/contacts/{id}")
def delete_contact(...)
```

**Power Platform Analogy:**
Standard operations in any Dataverse table.

---

### Pattern 2: Request → Validate → Process → Response

Every endpoint follows this flow:

1. **Request arrives** (HTTP)
2. **FastAPI validates** (Pydantic models)
3. **Your code processes** (business logic)
4. **FastAPI responds** (JSON)

**Power Platform Analogy:**
Like Power Automate flow steps:
1. Trigger received
2. Parse JSON / Schema validation
3. Conditions & actions
4. Response action

---

### Pattern 3: Decorators

```python
@app.post("/contacts")
def create_contact(...):
    ...
```

The `@` decorator **wraps** the function with extra behavior.

**What it does:**
- Registers the route with FastAPI
- Sets up HTTP method
- Configures validation
- Handles errors automatically

**Power Platform Analogy:**
Like putting an action inside a "Scope" in Power Automate - adds structure around it.

---

## 🚀 Next Steps

### Beginner Level ✅
- [x] Understand REST APIs
- [x] Know HTTP methods
- [x] Use Pydantic models
- [x] Handle errors

**Next:** Try modifying `main.py` to add a new field

---

### Intermediate Level 🎯
- [ ] Add a new endpoint (e.g., GET /contacts/count)
- [ ] Add a "favorite" boolean field
- [ ] Implement pagination (limit & offset)
- [ ] Add data persistence (SQLite)

**Next:** Study [TDD_GUIDE.md](TDD_GUIDE.md) and write tests first

---

### Advanced Level 🔥
- [ ] Add authentication (JWT tokens)
- [ ] Integrate with real database (PostgreSQL)
- [ ] Deploy to cloud (Azure/AWS)
- [ ] Add WebSocket support
- [ ] Create Power Platform Custom Connector

**Next:** Explore FastAPI's advanced features

---

## 📚 Recommended Learning Path

1. **Week 1:** Understand the basics
   - Read all comments in `main.py`
   - Complete all hands-on exercises
   - Experiment with API docs

2. **Week 2:** Modify the code
   - Add new fields to contacts
   - Create new endpoints
   - Write tests for your changes

3. **Week 3:** Build something new
   - Create a different API (Todo list, Notes, etc.)
   - Apply same patterns learned here
   - Integrate with Power Platform

4. **Week 4:** Advanced topics
   - Add database persistence
   - Implement authentication
   - Deploy to production

---

## 🤔 Common Questions

### Q: How is this different from Custom Connectors?
**A:** With Custom Connectors, you connect to *someone else's* API. Here, you're *building* the API yourself. You control everything!

### Q: Why learn this if I use Power Platform?
**A:**
- Build custom backends for complex logic
- Create APIs that multiple apps can use
- Have full control over data and performance
- Expand your technical skills

### Q: Is Python hard to learn?
**A:** If you know Power Fx formulas, you'll find Python familiar. Both use:
- Variables
- Functions
- Conditions (if/else)
- Loops (ForAll → for)

### Q: When would I use FastAPI vs Power Automate?
**A:**
- **FastAPI:** Complex logic, high performance, reusable APIs
- **Power Automate:** Quick automation, Microsoft ecosystem, low-code

They complement each other! Build FastAPI backends, call them from Power Platform.

---

## 💡 Tips for Success

1. **Don't rush** - Understand each concept before moving on
2. **Experiment** - Break things, see what happens, fix them
3. **Read the code** - `main.py` has detailed comments
4. **Use the docs** - http://localhost:8000/docs is your friend
5. **Ask questions** - Share with your team

---

**Happy Learning! 🚀**

The best way to learn is by doing. Start experimenting with the code today!
