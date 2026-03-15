# 📡 API Usage Examples

Practical examples for calling the Contact Book API from various tools and platforms.

---

## 🌐 Base URL

```
http://localhost:8000
```

When deployed, replace with your production URL (e.g., `https://your-api.azurewebsites.net`)

---

## 📋 Table of Contents

1. [Using Browser / Swagger UI](#using-browser--swagger-ui)
2. [Using curl (Command Line)](#using-curl-command-line)
3. [Using PowerShell](#using-powershell)
4. [Using Power Automate](#using-power-automate)
5. [Using JavaScript](#using-javascript)
6. [Using Python](#using-python)

---

## 🌐 Using Browser / Swagger UI

### **Easiest Method - Interactive API Docs**

1. Open: **http://localhost:8000/docs**
2. Click any endpoint to expand
3. Click **"Try it out"**
4. Fill in parameters
5. Click **"Execute"**
6. See request & response

**Perfect for:** Quick testing, learning, exploring

---

## 💻 Using curl (Command Line)

### **1. Create a Contact**

```bash
curl -X POST "http://localhost:8000/contacts" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "phone": "555-0101",
    "notes": "Met at conference"
  }'
```

**Response:**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "phone": "555-0101",
  "notes": "Met at conference"
}
```

---

### **2. List All Contacts**

```bash
curl -X GET "http://localhost:8000/contacts"
```

**Response:**
```json
[
  {
    "id": "a1b2c3d4...",
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "phone": "555-0101",
    "notes": "Met at conference"
  },
  {
    "id": "b2c3d4e5...",
    "name": "Bob Smith",
    "email": "bob@example.com",
    "phone": "555-0202",
    "notes": "College friend"
  }
]
```

---

### **3. Search Contacts**

```bash
curl -X GET "http://localhost:8000/contacts?q=alice"
```

**Response:** (Filtered list of contacts matching "alice")

---

### **4. Get Single Contact**

```bash
curl -X GET "http://localhost:8000/contacts/a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

**Response:** (Single contact object)

---

### **5. Update Contact (Partial)**

```bash
curl -X PUT "http://localhost:8000/contacts/a1b2c3d4-e5f6-7890-abcd-ef1234567890" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice.new@example.com"
  }'
```

**Note:** Only updates email, leaves other fields unchanged.

---

### **6. Delete Contact**

```bash
curl -X DELETE "http://localhost:8000/contacts/a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

**Response:**
```json
{
  "message": "Contact deleted"
}
```

---

## 🔵 Using PowerShell

### **1. Create a Contact**

```powershell
$body = @{
    name = "Charlie Davis"
    email = "charlie@example.com"
    phone = "555-0303"
    notes = "Potential client"
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://localhost:8000/contacts" `
  -Method Post `
  -Body $body `
  -ContentType "application/json"
```

---

### **2. List All Contacts**

```powershell
$contacts = Invoke-RestMethod `
  -Uri "http://localhost:8000/contacts" `
  -Method Get

$contacts | Format-Table
```

---

### **3. Search Contacts**

```powershell
$results = Invoke-RestMethod `
  -Uri "http://localhost:8000/contacts?q=charlie" `
  -Method Get

$results
```

---

### **4. Get Single Contact**

```powershell
$contactId = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

$contact = Invoke-RestMethod `
  -Uri "http://localhost:8000/contacts/$contactId" `
  -Method Get

$contact
```

---

### **5. Update Contact**

```powershell
$contactId = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
$updates = @{
    email = "charlie.updated@example.com"
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://localhost:8000/contacts/$contactId" `
  -Method Put `
  -Body $updates `
  -ContentType "application/json"
```

---

### **6. Delete Contact**

```powershell
$contactId = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

Invoke-RestMethod `
  -Uri "http://localhost:8000/contacts/$contactId" `
  -Method Delete
```

---

## ⚡ Using Power Automate

### **1. Create Contact Flow**

**Trigger:** Manual trigger or schedule

**Action:** HTTP

```
Method: POST
URI: http://localhost:8000/contacts
Headers:
  Content-Type: application/json
Body:
{
  "name": "@{triggerBody()?['name']}",
  "email": "@{triggerBody()?['email']}",
  "phone": "@{triggerBody()?['phone']}",
  "notes": "@{triggerBody()?['notes']}"
}
```

**Parse JSON (Response):**
```json
{
  "type": "object",
  "properties": {
    "id": { "type": "string" },
    "name": { "type": "string" },
    "email": { "type": "string" },
    "phone": { "type": "string" },
    "notes": { "type": "string" }
  }
}
```

---

### **2. List Contacts Flow**

**Action:** HTTP

```
Method: GET
URI: http://localhost:8000/contacts
```

**Parse JSON (Response):**
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "id": { "type": "string" },
      "name": { "type": "string" },
      "email": { "type": "string" },
      "phone": { "type": "string" },
      "notes": { "type": "string" }
    }
  }
}
```

**Apply to each:** Loop through the array

---

### **3. Search Contacts Flow**

**Action:** HTTP

```
Method: GET
URI: http://localhost:8000/contacts?q=@{variables('searchQuery')}
```

---

### **4. Update Contact Flow**

**Action:** HTTP

```
Method: PUT
URI: http://localhost:8000/contacts/@{variables('contactId')}
Headers:
  Content-Type: application/json
Body:
{
  "email": "@{triggerBody()?['newEmail']}"
}
```

---

### **5. Delete Contact Flow**

**Action:** HTTP

```
Method: DELETE
URI: http://localhost:8000/contacts/@{variables('contactId')}
```

---

## 🟨 Using JavaScript

### **1. Create Contact (fetch API)**

```javascript
async function createContact() {
  const response = await fetch('http://localhost:8000/contacts', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: 'Diana Prince',
      email: 'diana@example.com',
      phone: '555-0404',
      notes: 'Superhero'
    })
  });

  const contact = await response.json();
  console.log('Created:', contact);
  return contact;
}

createContact();
```

---

### **2. List All Contacts**

```javascript
async function listContacts() {
  const response = await fetch('http://localhost:8000/contacts');
  const contacts = await response.json();

  console.log('Total contacts:', contacts.length);
  contacts.forEach(c => console.log(c.name));

  return contacts;
}

listContacts();
```

---

### **3. Search Contacts**

```javascript
async function searchContacts(query) {
  const response = await fetch(
    `http://localhost:8000/contacts?q=${encodeURIComponent(query)}`
  );
  const results = await response.json();

  console.log(`Found ${results.length} matches`);
  return results;
}

searchContacts('diana');
```

---

### **4. Update Contact**

```javascript
async function updateContact(id, updates) {
  const response = await fetch(`http://localhost:8000/contacts/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updates)
  });

  const updated = await response.json();
  console.log('Updated:', updated);
  return updated;
}

updateContact('abc-123', { email: 'new@example.com' });
```

---

### **5. Delete Contact**

```javascript
async function deleteContact(id) {
  const response = await fetch(`http://localhost:8000/contacts/${id}`, {
    method: 'DELETE'
  });

  const result = await response.json();
  console.log(result.message);
}

deleteContact('abc-123');
```

---

## 🐍 Using Python

### **1. Create Contact (requests library)**

```python
import requests

url = "http://localhost:8000/contacts"
data = {
    "name": "Eve Wilson",
    "email": "eve@example.com",
    "phone": "555-0505",
    "notes": "Data scientist"
}

response = requests.post(url, json=data)
contact = response.json()

print(f"Created contact: {contact['id']}")
```

---

### **2. List All Contacts**

```python
import requests

response = requests.get("http://localhost:8000/contacts")
contacts = response.json()

for contact in contacts:
    print(f"{contact['name']} - {contact['email']}")
```

---

### **3. Search Contacts**

```python
import requests

params = {"q": "eve"}
response = requests.get("http://localhost:8000/contacts", params=params)
results = response.json()

print(f"Found {len(results)} matches")
```

---

### **4. Update Contact**

```python
import requests

contact_id = "abc-123-def-456"
updates = {"email": "eve.updated@example.com"}

response = requests.put(
    f"http://localhost:8000/contacts/{contact_id}",
    json=updates
)

updated = response.json()
print(f"Updated: {updated}")
```

---

### **5. Delete Contact**

```python
import requests

contact_id = "abc-123-def-456"
response = requests.delete(f"http://localhost:8000/contacts/{contact_id}")
result = response.json()

print(result["message"])
```

---

## 🧪 Testing with Postman

### **Import as Collection**

1. Open Postman
2. Click **Import**
3. Select **Raw text**
4. Paste this JSON:

```json
{
  "info": {
    "name": "Contact Book API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Create Contact",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"name\": \"Test Contact\",\n  \"email\": \"test@example.com\",\n  \"phone\": \"555-0000\",\n  \"notes\": \"Test notes\"\n}"
        },
        "url": "http://localhost:8000/contacts"
      }
    },
    {
      "name": "List Contacts",
      "request": {
        "method": "GET",
        "url": "http://localhost:8000/contacts"
      }
    },
    {
      "name": "Search Contacts",
      "request": {
        "method": "GET",
        "url": {
          "raw": "http://localhost:8000/contacts?q={{searchQuery}}",
          "query": [{"key": "q", "value": "{{searchQuery}}"}]
        }
      }
    }
  ]
}
```

---

## 🎯 Common Scenarios

### **Scenario 1: Bulk Create Contacts**

```python
import requests

contacts_data = [
    {"name": "Person 1", "email": "person1@test.com"},
    {"name": "Person 2", "email": "person2@test.com"},
    {"name": "Person 3", "email": "person3@test.com"}
]

for data in contacts_data:
    response = requests.post("http://localhost:8000/contacts", json=data)
    print(f"Created: {response.json()['id']}")
```

---

### **Scenario 2: Export All Contacts to CSV**

```python
import requests
import csv

# Get all contacts
response = requests.get("http://localhost:8000/contacts")
contacts = response.json()

# Write to CSV
with open('contacts.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'name', 'email', 'phone', 'notes'])
    writer.writeheader()
    writer.writerows(contacts)

print(f"Exported {len(contacts)} contacts to contacts.csv")
```

---

### **Scenario 3: Find and Update Multiple Contacts**

```python
import requests

# Find all contacts with gmail
response = requests.get("http://localhost:8000/contacts?q=gmail")
gmail_contacts = response.json()

# Update each one
for contact in gmail_contacts:
    updates = {"notes": "Uses Gmail"}
    requests.put(
        f"http://localhost:8000/contacts/{contact['id']}",
        json=updates
    )

print(f"Updated {len(gmail_contacts)} Gmail contacts")
```

---

## 🔍 Response Status Codes

Check HTTP status codes to handle errors:

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 201 | Created | Extract ID from response |
| 404 | Not Found | Contact doesn't exist |
| 422 | Validation Error | Check required fields |
| 500 | Server Error | Check logs, retry later |

---

## 💡 Tips

1. **Always check response status** before processing
2. **Use try-catch** for error handling
3. **Store API URL in variable** for easy changes
4. **Encode special characters** in URLs (use `encodeURIComponent`)
5. **Parse JSON responses** before using

---

**Happy API Calling! 🚀**

Need help? Check [README.md](README.md) or consult your team.
