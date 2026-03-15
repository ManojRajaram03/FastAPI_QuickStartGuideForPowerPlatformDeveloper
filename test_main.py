"""
Contact Book API — Test Suite (TDD)
====================================
These tests are written BEFORE the implementation.
Your job: make all these tests pass by building the FastAPI app.

Run tests:  pytest test_main.py -v
Run watch:  pytest test_main.py -v --tb=short -x  (stops at first failure)

Tests cover:
  1. Creating contacts (POST /contacts)
  2. Listing contacts (GET /contacts)
  3. Searching contacts (GET /contacts?q=...)
  4. Getting a single contact (GET /contacts/{id})
  5. Updating a contact (PUT /contacts/{id})
  6. Deleting a contact (DELETE /contacts/{id})
  7. Validation & error handling
"""

import pytest
from fastapi.testclient import TestClient

# This import will fail until you create main.py with the FastAPI app
from main import app


# ──────────────────────────────────────────────
# FIXTURES — shared setup for tests
# ──────────────────────────────────────────────

@pytest.fixture
def client():
    """
    Creates a test client that talks to your FastAPI app
    WITHOUT needing a running server. This is how FastAPI
    apps are tested — no real HTTP, just simulated requests.
    """
    return TestClient(app)


@pytest.fixture
def sample_contact():
    """A valid contact payload for reuse across tests."""
    return {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "phone": "312-555-0101",
        "notes": "Met at PyCon 2025"
    }


@pytest.fixture
def another_contact():
    """A second contact for multi-contact tests."""
    return {
        "name": "Bob Smith",
        "email": "bob@example.com",
        "phone": "773-555-0202",
        "notes": "College friend"
    }


def create_contact(client, contact_data):
    """Helper: creates a contact and returns the response JSON."""
    resp = client.post("/contacts", json=contact_data)
    assert resp.status_code == 201
    return resp.json()


# ──────────────────────────────────────────────
# TEST GROUP 1: Create contacts (POST /contacts)
# ──────────────────────────────────────────────

class TestCreateContact:
    """
    POST /contacts should accept a JSON body and return
    the created contact with a server-generated 'id' field.
    """

    def test_create_contact_returns_201(self, client, sample_contact):
        """Successful creation should return HTTP 201 Created."""
        resp = client.post("/contacts", json=sample_contact)
        assert resp.status_code == 201

    def test_create_contact_returns_id(self, client, sample_contact):
        """The response must include a unique 'id' field."""
        resp = client.post("/contacts", json=sample_contact)
        data = resp.json()
        assert "id" in data
        assert isinstance(data["id"], str)
        assert len(data["id"]) > 0

    def test_create_contact_echoes_fields(self, client, sample_contact):
        """The response should echo back all the fields we sent."""
        resp = client.post("/contacts", json=sample_contact)
        data = resp.json()
        assert data["name"] == "Alice Johnson"
        assert data["email"] == "alice@example.com"
        assert data["phone"] == "312-555-0101"
        assert data["notes"] == "Met at PyCon 2025"

    def test_create_contact_minimal_fields(self, client):
        """Only 'name' is required. Other fields are optional."""
        resp = client.post("/contacts", json={"name": "Charlie"})
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Charlie"
        assert data["email"] is None
        assert data["phone"] is None
        assert data["notes"] is None

    def test_create_contact_missing_name_fails(self, client):
        """Name is required — omitting it should return 422."""
        resp = client.post("/contacts", json={"email": "no-name@test.com"})
        assert resp.status_code == 422

    def test_create_two_contacts_get_unique_ids(self, client, sample_contact, another_contact):
        """Each contact must get a unique ID."""
        resp1 = client.post("/contacts", json=sample_contact)
        resp2 = client.post("/contacts", json=another_contact)
        assert resp1.json()["id"] != resp2.json()["id"]


# ──────────────────────────────────────────────
# TEST GROUP 2: List contacts (GET /contacts)
# ──────────────────────────────────────────────

class TestListContacts:
    """
    GET /contacts should return a list of all contacts.
    """

    def test_list_empty_returns_empty_list(self, client):
        """When no contacts exist, return an empty list."""
        resp = client.get("/contacts")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_returns_created_contacts(self, client, sample_contact, another_contact):
        """After creating contacts, they should appear in the list."""
        create_contact(client, sample_contact)
        create_contact(client, another_contact)

        resp = client.get("/contacts")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        names = [c["name"] for c in data]
        assert "Alice Johnson" in names
        assert "Bob Smith" in names


# ──────────────────────────────────────────────
# TEST GROUP 3: Search contacts (GET /contacts?q=)
# ──────────────────────────────────────────────

class TestSearchContacts:
    """
    GET /contacts?q=<query> should filter contacts.
    Search should match against name, email, phone, and notes.
    Search should be case-insensitive.
    """

    def test_search_by_name(self, client, sample_contact, another_contact):
        """Searching by name should return matching contacts."""
        create_contact(client, sample_contact)
        create_contact(client, another_contact)

        resp = client.get("/contacts", params={"q": "Alice"})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["name"] == "Alice Johnson"

    def test_search_by_email(self, client, sample_contact, another_contact):
        """Searching should also match email addresses."""
        create_contact(client, sample_contact)
        create_contact(client, another_contact)

        resp = client.get("/contacts", params={"q": "bob@example"})
        data = resp.json()
        assert len(data) == 1
        assert data[0]["name"] == "Bob Smith"

    def test_search_by_notes(self, client, sample_contact, another_contact):
        """Searching should match content in the notes field."""
        create_contact(client, sample_contact)
        create_contact(client, another_contact)

        resp = client.get("/contacts", params={"q": "PyCon"})
        data = resp.json()
        assert len(data) == 1
        assert data[0]["name"] == "Alice Johnson"

    def test_search_case_insensitive(self, client, sample_contact):
        """Search should be case-insensitive."""
        create_contact(client, sample_contact)

        resp = client.get("/contacts", params={"q": "alice"})
        assert len(resp.json()) == 1

        resp = client.get("/contacts", params={"q": "ALICE"})
        assert len(resp.json()) == 1

    def test_search_no_match_returns_empty(self, client, sample_contact):
        """Search with no matches should return an empty list, not an error."""
        create_contact(client, sample_contact)

        resp = client.get("/contacts", params={"q": "zzz_no_match"})
        assert resp.status_code == 200
        assert resp.json() == []

    def test_empty_search_returns_all(self, client, sample_contact, another_contact):
        """An empty query string should return all contacts."""
        create_contact(client, sample_contact)
        create_contact(client, another_contact)

        resp = client.get("/contacts", params={"q": ""})
        assert len(resp.json()) == 2


# ──────────────────────────────────────────────
# TEST GROUP 4: Get single contact (GET /contacts/{id})
# ──────────────────────────────────────────────

class TestGetContact:
    """
    GET /contacts/{id} should return a single contact by its ID.
    """

    def test_get_existing_contact(self, client, sample_contact):
        """Fetching a valid ID should return that contact."""
        created = create_contact(client, sample_contact)
        contact_id = created["id"]

        resp = client.get(f"/contacts/{contact_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == contact_id
        assert data["name"] == "Alice Johnson"

    def test_get_nonexistent_contact_returns_404(self, client):
        """Fetching a non-existent ID should return 404."""
        resp = client.get("/contacts/fake-id-does-not-exist")
        assert resp.status_code == 404


# ──────────────────────────────────────────────
# TEST GROUP 5: Update contact (PUT /contacts/{id})
# ──────────────────────────────────────────────

class TestUpdateContact:
    """
    PUT /contacts/{id} should update an existing contact.
    Only the fields provided in the body should change.
    """

    def test_update_name(self, client, sample_contact):
        """Updating the name should persist the change."""
        created = create_contact(client, sample_contact)
        contact_id = created["id"]

        resp = client.put(f"/contacts/{contact_id}", json={"name": "Alice Wu"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Alice Wu"

        # Verify it persisted
        get_resp = client.get(f"/contacts/{contact_id}")
        assert get_resp.json()["name"] == "Alice Wu"

    def test_update_preserves_other_fields(self, client, sample_contact):
        """Updating one field should NOT wipe out other fields."""
        created = create_contact(client, sample_contact)
        contact_id = created["id"]

        client.put(f"/contacts/{contact_id}", json={"notes": "Updated note"})

        get_resp = client.get(f"/contacts/{contact_id}")
        data = get_resp.json()
        assert data["notes"] == "Updated note"
        assert data["name"] == "Alice Johnson"       # unchanged
        assert data["email"] == "alice@example.com"   # unchanged
        assert data["phone"] == "312-555-0101"        # unchanged

    def test_update_multiple_fields(self, client, sample_contact):
        """Should be able to update multiple fields at once."""
        created = create_contact(client, sample_contact)
        contact_id = created["id"]

        resp = client.put(f"/contacts/{contact_id}", json={
            "email": "newalice@example.com",
            "phone": "555-999-0000"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "newalice@example.com"
        assert data["phone"] == "555-999-0000"

    def test_update_nonexistent_returns_404(self, client):
        """Updating a non-existent contact should return 404."""
        resp = client.put("/contacts/fake-id", json={"name": "Ghost"})
        assert resp.status_code == 404


# ──────────────────────────────────────────────
# TEST GROUP 6: Delete contact (DELETE /contacts/{id})
# ──────────────────────────────────────────────

class TestDeleteContact:
    """
    DELETE /contacts/{id} should remove a contact permanently.
    """

    def test_delete_existing_contact(self, client, sample_contact):
        """Deleting should return 200 and a confirmation message."""
        created = create_contact(client, sample_contact)
        contact_id = created["id"]

        resp = client.delete(f"/contacts/{contact_id}")
        assert resp.status_code == 200
        assert "deleted" in resp.json().get("message", "").lower()

    def test_delete_removes_from_list(self, client, sample_contact, another_contact):
        """After deletion, the contact should no longer appear in the list."""
        created = create_contact(client, sample_contact)
        create_contact(client, another_contact)
        contact_id = created["id"]

        client.delete(f"/contacts/{contact_id}")

        resp = client.get("/contacts")
        names = [c["name"] for c in resp.json()]
        assert "Alice Johnson" not in names
        assert "Bob Smith" in names

    def test_delete_makes_get_return_404(self, client, sample_contact):
        """After deletion, fetching that ID should return 404."""
        created = create_contact(client, sample_contact)
        contact_id = created["id"]

        client.delete(f"/contacts/{contact_id}")

        resp = client.get(f"/contacts/{contact_id}")
        assert resp.status_code == 404

    def test_delete_nonexistent_returns_404(self, client):
        """Deleting a non-existent contact should return 404."""
        resp = client.delete("/contacts/fake-id")
        assert resp.status_code == 404


# ──────────────────────────────────────────────
# TEST GROUP 7: Edge cases & validation
# ──────────────────────────────────────────────

class TestEdgeCases:
    """
    Tests for boundary conditions and data integrity.
    """

    def test_create_contact_with_empty_name_fails(self, client):
        """An empty string for name should fail validation (422)."""
        resp = client.post("/contacts", json={"name": ""})
        assert resp.status_code == 422

    def test_create_contact_with_whitespace_name_fails(self, client):
        """A name that is only whitespace should fail validation (422)."""
        resp = client.post("/contacts", json={"name": "   "})
        assert resp.status_code == 422

    def test_contacts_are_isolated_between_tests(self, client):
        """
        Each test should start with a clean slate.
        This test verifies the contact list is empty — meaning
        the store resets between tests.

        IMPLEMENTATION NOTE: You'll need a way to reset the
        in-memory store between tests. One approach is to use
        a pytest fixture that clears the store, or make the
        app use dependency injection for the store.
        """
        resp = client.get("/contacts")
        assert resp.json() == []
