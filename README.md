# 📇 Contact Book API - FastAPI Learning Project

A fully-functional REST API built with **FastAPI** for managing contacts. Designed specifically for **Power Platform developers** learning modern Python web development.

---

## 🎯 What You'll Learn

- ✅ Building REST APIs with FastAPI
- ✅ Pydantic models for data validation (like Dataverse tables)
- ✅ HTTP methods (GET, POST, PUT, DELETE)
- ✅ Path parameters, query parameters, request bodies
- ✅ Error handling and status codes
- ✅ Test-Driven Development (TDD) with pytest
- ✅ CORS configuration for frontend integration
- ✅ Auto-generated API documentation

**Perfect for:** Power Platform developers wanting to expand into code-first development.

---

## 📋 Prerequisites

Before you start, ensure you have:

- [ ] **Python 3.9+** installed ([Download here](https://www.python.org/downloads/))
  - Check version: `python --version`
- [ ] **pip** (Python package manager - comes with Python)
  - Check version: `pip --version`
- [ ] A **code editor** (VS Code recommended)
- [ ] A **web browser** (Chrome, Edge, Firefox)
- [ ] **Basic terminal/command prompt** knowledge

---

## 🚀 Quick Start (5 Minutes)

### **Step 1: Install Dependencies**

Open terminal in the project folder and run:

```bash
pip install fastapi uvicorn pytest httpx
```

### **Step 2: Start the Backend API**

```bash
uvicorn main:app --reload
```

✅ Backend running at: **http://localhost:8000**
✅ API Documentation: **http://localhost:8000/docs**

### **Step 3: Start the Frontend** (New terminal window)

```bash
python -m http.server 5500
```

✅ Frontend running at: **http://localhost:5500**

### **Step 4: Open in Browser**

Visit **http://localhost:5500** and start creating contacts!

---

## 📁 Project Structure

```
FastAPI/
├── main.py              # Backend API (heavily commented for learning)
├── conftest.py          # Test configuration (test isolation)
├── test_main.py         # 27 automated tests (all passing ✅)
├── index.html           # Frontend UI (single-file app)
│
├── README.md            # ← You are here
├── QUICKSTART.md        # Express setup guide
├── LEARNING_GUIDE.md    # Educational resource
├── API_EXAMPLES.md      # Practical API usage examples
├── CLAUDE.md            # Context for AI assistants
└── TDD_GUIDE.md         # Test-Driven Development guide
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/contacts` | Create a new contact |
| GET | `/contacts` | List all contacts (with optional `?q=` search) |
| GET | `/contacts/{id}` | Get a specific contact by ID |
| PUT | `/contacts/{id}` | Update a contact (partial updates supported) |
| DELETE | `/contacts/{id}` | Delete a contact |

**📖 For detailed examples, see [API_EXAMPLES.md](API_EXAMPLES.md)**

---

## 🧪 Running Tests

The project includes 27 automated tests covering all functionality.

### Run all tests:
```bash
pytest test_main.py -v
```

### Run specific test class:
```bash
pytest test_main.py::TestCreateContact -v
```

### Run with detailed output:
```bash
pytest test_main.py -v --tb=short
```

**Expected result:** ✅ **27 passed**

---

## 💡 How to Use

### **Option 1: Use the Web UI** (Easiest)
1. Open http://localhost:5500
2. Add, search, edit, and delete contacts through the interface

### **Option 2: Use API Documentation** (Interactive)
1. Open http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Fill in parameters and execute requests
4. See real-time responses

### **Option 3: Use Code/Scripts** (Power Automate-style)
See [API_EXAMPLES.md](API_EXAMPLES.md) for:
- curl commands
- PowerShell examples
- Power Automate HTTP action configurations
- JavaScript fetch() examples

---

## 🎓 Learning Path

### **For Complete Beginners:**
1. Start with [QUICKSTART.md](QUICKSTART.md) - Get it running
2. Open http://localhost:8000/docs - Explore the API
3. Read [LEARNING_GUIDE.md](LEARNING_GUIDE.md) - Understand concepts
4. Open `main.py` - Read the detailed comments
5. Try [API_EXAMPLES.md](API_EXAMPLES.md) - Make API calls

### **For Power Platform Developers:**
1. Read the "Power Platform Analogies" in `main.py`
2. Compare REST API concepts to Custom Connectors
3. See how Pydantic models relate to Dataverse tables
4. Understand how this could integrate with Power Automate

### **For Advanced Users:**
1. Read [TDD_GUIDE.md](TDD_GUIDE.md) - Test-Driven Development
2. Study `test_main.py` - Learn testing patterns
3. Modify the code - Add new features
4. Run tests to ensure nothing breaks

---

## 🔧 Troubleshooting

### **Port Already in Use**
**Error:** `Address already in use`

**Solution:**
```bash
# Use different ports
uvicorn main:app --reload --port 8001
python -m http.server 5501
```
Then update API_URL in `index.html` line 200.

### **Module Not Found**
**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
pip install fastapi uvicorn pytest httpx
```

### **Tests Failing**
**Error:** Tests don't pass

**Solution:**
1. Ensure you're in the project directory
2. Check that `main.py` hasn't been modified
3. Run: `pytest test_main.py -v --tb=long` for detailed errors

### **Frontend Not Connecting to API**
**Error:** Network errors in browser console

**Solutions:**
1. Ensure backend is running on port 8000
2. Check CORS is enabled in `main.py` (line 19-25)
3. Open browser console (F12) for specific error messages

### **Data Disappears After Restart**
**Not an error!** The database is in-memory only. Data resets when you restart the server.

To persist data, you'd need to integrate a real database (SQLite, PostgreSQL, etc.).

---

## 📚 Additional Resources

### **Documentation:**
- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [pytest Documentation](https://docs.pytest.org/)

### **Learn More:**
- [REST API Basics](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [JSON Basics](https://www.json.org/)

### **Power Platform Integration:**
- [Custom Connectors](https://learn.microsoft.com/en-us/connectors/custom-connectors/)
- [HTTP Connector in Power Automate](https://learn.microsoft.com/en-us/power-automate/http-connector)

---

## 🎯 Next Steps

After mastering this project:

1. **Add Features:**
   - Add categories/tags to contacts
   - Add a "favorite" flag
   - Add created/updated timestamps
   - Add pagination for large lists

2. **Add Persistence:**
   - Replace in-memory list with SQLite
   - Use SQLAlchemy ORM
   - Try cloud databases (Azure SQL, Cosmos DB)

3. **Add Authentication:**
   - Implement JWT tokens
   - Add user login/registration
   - Protect endpoints with authentication

4. **Deploy to Cloud:**
   - Deploy to Azure App Service
   - Use Azure Functions
   - Containerize with Docker

5. **Integrate with Power Platform:**
   - Create a Custom Connector in Power Apps
   - Build a Power Automate flow that calls this API
   - Create a Power BI report using the API

---

## 🤝 Contributing

This is a learning project! Feel free to:
- Experiment with the code
- Add new features
- Share improvements with the team
- Ask questions

---

## 📝 License

This is an educational project for internal team use.

---

## 🆘 Need Help?

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the detailed comments in `main.py`
3. Consult [LEARNING_GUIDE.md](LEARNING_GUIDE.md)
4. Ask your team members

---

**Happy Learning! 🚀**

Built with ❤️ for Power Platform developers exploring FastAPI.
