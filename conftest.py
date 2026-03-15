"""
Pytest configuration file.

Key Learning:
- conftest.py is automatically discovered by pytest
- Fixtures defined here are available to all tests
- autouse=True makes a fixture run automatically before each test
"""

import pytest


@pytest.fixture(autouse=True)
def reset_database():
    """
    Reset the in-memory database before each test.

    Key Learning:
    - This solves the "test isolation" problem
    - Without this, contacts created in one test leak into others
    - autouse=True means this runs before EVERY test automatically
    - We import here to avoid circular imports
    """
    from main import contacts_db
    contacts_db.clear()
