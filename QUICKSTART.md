# ⚡ Quick Start Guide

Get the Contact Book API running in **5 minutes**. No explanations, just commands.

---

## ✅ Prerequisites Check

```bash
python --version    # Should be 3.9 or higher
pip --version       # Should show a version number
```

If either command fails, [install Python](https://www.python.org/downloads/) first.

---

## 📦 Step 1: Install Dependencies

```bash
pip install fastapi uvicorn pytest httpx
```

⏱️ Takes ~30 seconds

---

## 🚀 Step 2: Start Backend

```bash
uvicorn main:app --reload
```

✅ You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Keep this terminal open!**

---

## 🌐 Step 3: Start Frontend

**Open a NEW terminal window** in the same folder:

```bash
python -m http.server 5500
```

✅ You should see:
```
Serving HTTP on 0.0.0.0 port 5500
```

**Keep this terminal open too!**

---

## 🎉 Step 4: Open in Browser

Click these links:

- **Frontend UI:** http://localhost:5500
- **API Docs:** http://localhost:8000/docs

---

## 🧪 (Optional) Run Tests

Open a **third terminal** and run:

```bash
pytest test_main.py -v
```

✅ Expected: `27 passed`

---

## 🛑 Stop the Servers

Press **Ctrl+C** in each terminal window.

---

## 🎯 What Next?

- ✅ Read [README.md](README.md) for full documentation
- ✅ Try [API_EXAMPLES.md](API_EXAMPLES.md) for API usage
- ✅ Study [LEARNING_GUIDE.md](LEARNING_GUIDE.md) to understand concepts
- ✅ Open `main.py` to see detailed code comments

---

## 🆘 Common Issues

### Port 8000 already in use?
```bash
uvicorn main:app --reload --port 8001
```
Then update `index.html` line 200: `const API_URL = 'http://localhost:8001';`

### Port 5500 already in use?
```bash
python -m http.server 5501
```
Then visit http://localhost:5501

### Dependencies won't install?
```bash
python -m pip install --upgrade pip
pip install fastapi uvicorn pytest httpx
```

---

**That's it! You're running a full-stack FastAPI application! 🚀**
