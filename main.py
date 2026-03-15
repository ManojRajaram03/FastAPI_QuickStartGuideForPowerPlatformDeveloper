# ============================================
# IMPORTS - Bringing in tools we need
# ============================================
# Think of imports like adding connectors in Power Automate
# We're bringing in pre-built functionality

from fastapi import FastAPI, HTTPException, status
# FastAPI - The main framework (like the Power Apps/Automate platform itself)
# HTTPException - For returning errors (like Terminate action in Power Automate)
# status - HTTP status codes as constants (200, 404, 422, etc.)

from fastapi.middleware.cors import CORSMiddleware
# CORSMiddleware - Allows browsers to call our API from different domains
# Similar to enabling API connections in Power Platform

from pydantic import BaseModel, field_validator
# BaseModel - Base class for creating data models (like Dataverse tables)
# field_validator - Decorator for custom validation (like business rules in Dataverse)

from typing import Optional
# Optional - Marks a field as "can be None" (like optional fields in Power Apps forms)

import uuid
# uuid - Generates unique IDs (like GUID() function in Power Apps)


# ============================================
# CREATE THE APP INSTANCE
# ============================================
# This is like creating a new Power Apps app or Power Automate flow
# Everything starts with this app object
app = FastAPI()  # FastAPI() creates a new web application


# ============================================
# CORS MIDDLEWARE (For browser-based frontends)
# ============================================
# POWER PLATFORM ANALOGY: Like configuring "Who can access this API" settings
# In Power Platform, you set permissions on apps/flows
# Here, we use CORS to control which websites can call our API

# What is Middleware?
# - Think of it like a "Pre-processing step" that runs BEFORE every API call
# - Similar to a "parent" flow that triggers before child flows in Power Automate
# - Every HTTP request passes through middleware first

app.add_middleware(  # .add_middleware() attaches middleware to the app
    CORSMiddleware,  # The type of middleware (CORS = Cross-Origin Resource Sharing)

    # allow_origins controls which websites can call this API
    # ["*"] = wildcard = allow ALL websites (only for development!)
    # In production, you'd specify exact URLs like ["https://mycompany.com"]
    allow_origins=["*"],

    # allow_credentials: If True, browser can send cookies/auth headers
    # Similar to enabling "Pass credentials" in Power Automate HTTP actions
    allow_credentials=True,

    # allow_methods: Which HTTP verbs are allowed (GET, POST, PUT, DELETE, etc.)
    # ["*"] = allow all methods
    allow_methods=["*"],

    # allow_headers: Which HTTP headers browsers can send
    # ["*"] = allow all headers (like Content-Type, Authorization, etc.)
    allow_headers=["*"],
)


# ============================================
# IN-MEMORY DATA STORAGE
# ============================================
# POWER PLATFORM ANALOGY: Like a Collection variable in Power Apps or a global variable
# This is a Python LIST (array) that stores all our contacts
# [] means empty list to start
# NOTE: This data disappears when the server restarts (no persistence)
# In production, you'd use a real database (SQL Server, Cosmos DB, etc.)
contacts_db = []  # Global variable - accessible from all functions below

# ============================================
# PYDANTIC MODELS (Data Validation & Schema)
# ============================================
# POWER PLATFORM ANALOGY: Like creating Tables in Dataverse or defining JSON schemas
# These models define the STRUCTURE and RULES for our data

# What is a Pydantic Model?
# - It's a CLASS that defines what fields exist and their data types
# - Automatically validates incoming data (like Form validation in Power Apps)
# - Generates API documentation automatically
# - Similar to creating a Dataverse table with columns and data types


class ContactCreate(BaseModel):
    """
    Model for CREATING a new contact (what the user sends us).

    POWER PLATFORM ANALOGY:
    - Like a Power Apps Edit Form with required/optional fields
    - Similar to a Parse JSON action schema in Power Automate
    - Defines what fields are required vs. optional
    """

    # FIELD DEFINITIONS - The colon syntax defines the data type
    # Format: field_name: data_type = default_value

    name: str
    # str = string/text type (required because no "= None")
    # POWER PLATFORM ANALOGY: Single line of text field marked as "Required" in Dataverse

    email: Optional[str] = None
    # Optional[str] = can be string OR None (null)
    # = None makes it optional (user doesn't have to provide it)
    # POWER PLATFORM ANALOGY: Optional email field in a Power Apps form

    phone: Optional[str] = None
    # Same as email - optional phone field

    location: Optional[str] = None
    # Optional location field (city, state, country, etc.)
    # POWER PLATFORM ANALOGY: Like an optional address/location field in a contact form

    notes: Optional[str] = None
    # Optional notes field for additional information


    # ========================================
    # CUSTOM VALIDATION - Like Business Rules
    # ========================================
    # POWER PLATFORM ANALOGY: Like a Business Rule in Dataverse or OnChange validation in Power Apps

    @field_validator('name')  # @ is a DECORATOR - it modifies the function below
    # @field_validator('name') means "run this function to validate the 'name' field"
    # Decorators are like "wrapping" a function with extra behavior
    # Think of it like adding a "Scope" or "Apply to each" around an action in Power Automate

    @classmethod  # This decorator marks it as a class method (technical requirement for validators)
    # You can ignore this for now - just know it's required for field validators

    def name_must_not_be_empty(cls, v: str) -> str:
        # Function name can be anything descriptive
        # cls = the class itself (ContactCreate) - not used here
        # v = the VALUE being validated (the actual name string sent by user)
        # -> str means this function RETURNS a string

        """Custom validation: Name cannot be empty or just whitespace."""

        # VALIDATION LOGIC
        if not v or not v.strip():
            # not v = checks if v is empty string "" or None
            # not v.strip() = checks if v is only whitespace "   "
            # .strip() removes leading/trailing spaces

            # If validation FAILS, raise an error
            raise ValueError('Name must not be empty or whitespace')
            # ValueError tells FastAPI "this data is invalid"
            # FastAPI automatically converts this to HTTP 422 (Unprocessable Entity)
            # POWER PLATFORM ANALOGY: Like showing "Required field" error in Power Apps

        # If validation PASSES, return the value
        return v  # Return the original value (or you could return a modified version)


class ContactResponse(BaseModel):
    """
    Model for RETURNING a contact to the user (what we send back).

    POWER PLATFORM ANALOGY:
    - Like the response schema in Power Automate's HTTP Response action
    - Or the Display Form in Power Apps showing all fields including auto-generated ones
    - Defines what the API returns (includes server-generated fields like 'id')

    WHY A SEPARATE MODEL?
    - ContactCreate = what user SENDS (no id, because we generate it)
    - ContactResponse = what we RETURN (includes id that we generated)
    """

    # Notice the difference: 'id' is REQUIRED here (no = None)
    id: str
    # The server generates this ID, so responses always have it
    # POWER PLATFORM ANALOGY: Like the auto-generated GUID in Dataverse records

    name: str
    # Required in response (because user had to provide it when creating)

    email: Optional[str] = None
    # Optional - might be None if user didn't provide it

    phone: Optional[str] = None
    # Optional phone field

    location: Optional[str] = None
    # Optional location field

    notes: Optional[str] = None
    # Optional notes field

    # FastAPI uses this model to:
    # 1. Validate our response (makes sure we return correct data)
    # 2. Generate API documentation (Swagger shows what fields are returned)
    # 3. Convert Python dict to JSON automatically


class ContactUpdate(BaseModel):
    """
    Model for UPDATING an existing contact (partial updates allowed).

    POWER PLATFORM ANALOGY:
    - Like an Edit Form in Power Apps where user can change some fields
    - Similar to a PATCH operation in Dataverse
    - All fields optional = user can update just email, or just phone, etc.

    KEY DIFFERENCE FROM ContactCreate:
    - ContactCreate: name is REQUIRED
    - ContactUpdate: name is OPTIONAL (because you might just want to update email)
    """

    # ALL fields are Optional[str] = None
    # This allows "partial updates" - update only the fields you want to change

    name: Optional[str] = None
    # Even name is optional now! User can update just email without touching name
    # POWER PLATFORM ANALOGY: Like using Patch() to update only specific columns

    email: Optional[str] = None
    # User can update email or leave it unchanged

    phone: Optional[str] = None
    # User can update phone or leave it unchanged

    location: Optional[str] = None
    # User can update location or leave it unchanged

    notes: Optional[str] = None
    # User can update notes or leave it unchanged

    # How FastAPI knows which fields to update?
    # We use .model_dump(exclude_unset=True) later
    # This gives us ONLY the fields the user actually sent
    # exclude_unset=True means "exclude fields that weren't set by the user"


# ============================================
# API ENDPOINTS - The actual API operations
# ============================================
# POWER PLATFORM ANALOGY: Each endpoint is like a separate flow in Power Automate
# Or like different screens/functions in a Power App


# ========================================
# ENDPOINT 1: CREATE CONTACT (POST)
# ========================================
# POWER PLATFORM ANALOGY:
# - Like a "When HTTP request is received" trigger in Power Automate
# - Or SubmitForm() function in Power Apps that creates a Dataverse record

@app.post("/contacts", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
# @ = DECORATOR - modifies the function below it
# @app.post() = "This function handles POST requests"

# DECORATOR PARAMETERS EXPLAINED:
# 1. "/contacts" = the URL path (endpoint address)
#    User calls: http://localhost:8000/contacts
#
# 2. response_model=ContactResponse
#    Tells FastAPI: "I will return a ContactResponse object"
#    - FastAPI validates the response matches this model
#    - Auto-generates API documentation
#    - Converts Python dict → JSON automatically
#
# 3. status_code=status.HTTP_201_CREATED
#    Sets HTTP status code to 201 (means "Created successfully")
#    status.HTTP_201_CREATED = constant = number 201
#    HTTP Status codes: 200=OK, 201=Created, 404=Not Found, 422=Validation Error

def create_contact(contact: ContactCreate):
    # This is a regular Python FUNCTION
    # FastAPI calls this function when a POST request arrives

    # FUNCTION PARAMETERS:
    # contact: ContactCreate
    #   - Parameter name is "contact"
    #   - Type hint is ": ContactCreate" (the Pydantic model we defined earlier)
    #   - FastAPI sees this and automatically:
    #     a) Takes the JSON from request body
    #     b) Validates it against ContactCreate model
    #     c) If valid, creates a ContactCreate object
    #     d) If invalid, returns 422 error automatically
    # POWER PLATFORM ANALOGY: Like parsing JSON in Power Automate, but automatic!

    """Create a new contact and return it with a generated ID."""

    # ========================================
    # STEP 1: Generate unique ID
    # ========================================
    contact_id = str(uuid.uuid4())
    # uuid.uuid4() = generates a random unique ID (like GUID() in Power Apps)
    # Returns something like: a1b2c3d4-e5f6-7890-abcd-ef1234567890
    # str() converts it to a string
    # POWER PLATFORM ANALOGY: GUID() function in Power Apps formulas


    # ========================================
    # STEP 2: Convert Pydantic model to dictionary
    # ========================================
    contact_data = contact.model_dump()
    # .model_dump() converts the Pydantic model → Python dictionary
    # Example result: {"name": "John", "email": "john@test.com", "phone": None, "notes": None}
    # We need a dict (not a Pydantic object) to store in our list

    contact_data["id"] = contact_id
    # Add the generated ID to the dictionary
    # Dictionary access: dict["key"] = value
    # POWER PLATFORM ANALOGY: Like adding a new property to a JSON object in Power Automate


    # ========================================
    # STEP 3: Store in database
    # ========================================
    contacts_db.append(contact_data)
    # .append() adds the new contact to the end of the list
    # contacts_db is our global list variable defined at the top
    # POWER PLATFORM ANALOGY: Like adding to a Collection in Power Apps: Collect(Contacts, NewRecord)


    # ========================================
    # STEP 4: Return the created contact
    # ========================================
    return contact_data
    # FastAPI automatically converts this dict → JSON
    # Validates it matches ContactResponse model
    # Sends HTTP response with status code 201
    # POWER PLATFORM ANALOGY: Like the "Respond to HTTP request" action in Power Automate


# ========================================
# ENDPOINT 2: LIST/SEARCH CONTACTS (GET)
# ========================================
# POWER PLATFORM ANALOGY:
# - Like a "Get items" action in Power Automate to retrieve Dataverse records
# - Or Gallery.Items property in Power Apps
# - Supports filtering like Filter() function in Power Apps

@app.get("/contacts", response_model=list[ContactResponse])
# @app.get() = handles GET requests (retrieving data, not changing it)
# SAME PATH as POST ("/contacts") but DIFFERENT HTTP METHOD
# HTTP Methods are like different actions on the same resource:
#   - POST /contacts = CREATE a contact
#   - GET /contacts = LIST contacts
# This is RESTful API design

# response_model=list[ContactResponse]
#   - list[] means we return an ARRAY/LIST of contacts
#   - [ContactResponse] means each item in the list is a ContactResponse object
#   - POWER PLATFORM ANALOGY: Like defining array schema in Parse JSON

def list_contacts(q: Optional[str] = None):
    # FUNCTION PARAMETER: q: Optional[str] = None
    # This becomes a QUERY PARAMETER in the URL
    # User calls: http://localhost:8000/contacts?q=john
    # FastAPI extracts "john" from ?q= and passes it as the 'q' parameter
    # = None makes it optional (user doesn't have to provide ?q=)
    # POWER PLATFORM ANALOGY: Like URL query parameters in HTTP request action

    """List all contacts, optionally filtered by search query."""

    # ========================================
    # STEP 1: Check if search query provided
    # ========================================
    if not q:
        # "not q" is True when:
        #   - q is None (user didn't provide ?q=)
        #   - q is empty string (user provided ?q= with nothing)
        # In both cases, return ALL contacts (no filtering)

        return contacts_db
        # Return the entire list
        # FastAPI converts this → JSON array automatically
        # POWER PLATFORM ANALOGY: Like returning all items from a Dataverse table


    # ========================================
    # STEP 2: Prepare for case-insensitive search
    # ========================================
    query_lower = q.lower()
    # .lower() converts string to lowercase: "JOHN" → "john"
    # This allows case-insensitive search
    # We'll compare this against lowercased field values

    filtered_contacts = []
    # Create empty list to store matching contacts
    # POWER PLATFORM ANALOGY: Like creating an empty Collection in Power Apps


    # ========================================
    # STEP 3: Loop through all contacts and filter
    # ========================================
    for contact in contacts_db:
        # "for contact in contacts_db" = loop through each contact
        # POWER PLATFORM ANALOGY: Like "Apply to each" in Power Automate

        # Check if query matches ANY field (name, email, phone, location, OR notes)
        # This is a complex IF condition with OR logic

        if (query_lower in (contact.get("name") or "").lower() or
            query_lower in (contact.get("email") or "").lower() or
            query_lower in (contact.get("phone") or "").lower() or
            query_lower in (contact.get("location") or "").lower() or
            query_lower in (contact.get("notes") or "").lower()):

            # Let's break down this complex condition:
            #
            # contact.get("name") = gets the "name" value from the contact dictionary
            #   - Returns None if "name" doesn't exist (safer than contact["name"])
            #
            # or "" = if contact.get("name") is None, use empty string instead
            #   - Prevents errors when calling .lower() on None
            #
            # .lower() = convert to lowercase for case-insensitive comparison
            #
            # query_lower in ... = checks if query_lower is INSIDE the field value
            #   - "jo" in "john" → True (substring match)
            #   - Like StartsWith() or Contains() in Power Apps
            #
            # or or or = if ANY condition is True, the whole thing is True
            #   - Searches across multiple fields

            # If match found, add to filtered list
            filtered_contacts.append(contact)
            # POWER PLATFORM ANALOGY: Like Filter() function checking multiple columns


    # ========================================
    # STEP 4: Return filtered results
    # ========================================
    return filtered_contacts
    # Return the list of matching contacts
    # Could be empty list [] if no matches (that's OK, not an error!)
    # FastAPI converts → JSON array automatically


# ========================================
# ENDPOINT 3: GET SINGLE CONTACT (GET by ID)
# ========================================
# POWER PLATFORM ANALOGY:
# - Like "Get record" action in Power Automate (get one specific record by ID)
# - Or LookUp() function in Power Apps: LookUp(Contacts, ID = "abc123")

@app.get("/contacts/{contact_id}", response_model=ContactResponse)
# @app.get() = GET request (retrieving data)

# PATH PARAMETER: {contact_id}
# Curly braces {} indicate a PATH PARAMETER (variable in the URL path)
# Example URLs:
#   - http://localhost:8000/contacts/abc-123 → contact_id = "abc-123"
#   - http://localhost:8000/contacts/xyz-789 → contact_id = "xyz-789"
# FastAPI extracts the value from URL and passes it to the function
# POWER PLATFORM ANALOGY: Like dynamic content in Power Automate URLs

# DIFFERENCE: Query param vs Path param
#   - Query param: ?q=value (optional, for filtering)
#   - Path param: /contacts/{id} (part of URL, identifies specific resource)

def get_contact(contact_id: str):
    # FUNCTION PARAMETER: contact_id: str
    # Name MUST match the {contact_id} in the path above
    # : str = type hint (FastAPI converts URL value to string)
    # FastAPI automatically extracts this from the URL

    """Get a single contact by its unique ID."""

    # ========================================
    # STEP 1: Search for the contact
    # ========================================
    for contact in contacts_db:
        # Loop through all contacts in our database
        # POWER PLATFORM ANALOGY: Like iterating through Dataverse records

        if contact["id"] == contact_id:
            # Check if this contact's ID matches what user requested
            # contact["id"] = get the "id" field from the contact dictionary
            # == is comparison operator (equals)

            # Found it! Return immediately
            return contact
            # FastAPI converts dict → JSON
            # Validates against ContactResponse model
            # Returns HTTP 200 (OK) automatically


    # ========================================
    # STEP 2: If we get here, contact wasn't found
    # ========================================
    # If the for loop completes without returning, the ID doesn't exist
    # We need to return an ERROR (HTTP 404 = Not Found)

    raise HTTPException(
        # "raise" = throw an exception (error)
        # HTTPException = special FastAPI exception for HTTP errors
        # POWER PLATFORM ANALOGY: Like "Terminate" action in Power Automate with error status

        status_code=status.HTTP_404_NOT_FOUND,
        # status.HTTP_404_NOT_FOUND = constant = number 404
        # 404 = "Resource Not Found" (standard HTTP error for missing data)
        # POWER PLATFORM ANALOGY: Like returning 404 from HTTP Response action

        detail=f"Contact with id {contact_id} not found"
        # detail = the error message shown to user
        # f"..." = f-string (formatted string) - allows embedding variables
        # {contact_id} inside the string gets replaced with the actual ID value
        # Example: f"Contact with id abc-123 not found"
        # POWER PLATFORM ANALOGY: Like using expressions in Power Automate strings
    )
    # When HTTPException is raised:
    # - FastAPI stops execution
    # - Returns HTTP 404 response
    # - JSON body: {"detail": "Contact with id abc-123 not found"}


# ========================================
# ENDPOINT 4: UPDATE CONTACT (PUT)
# ========================================
# POWER PLATFORM ANALOGY:
# - Like "Update a record" action in Power Automate
# - Or Patch() function in Power Apps to update specific fields

@app.put("/contacts/{contact_id}", response_model=ContactResponse)
# @app.put() = PUT request (updating existing data)
# PUT = "Update this resource"
# Note: Some APIs use PATCH for partial updates and PUT for full replacement
# We're using PUT with partial update capability

# TWO INPUTS:
# 1. {contact_id} = PATH PARAMETER (which contact to update)
# 2. Request body = ContactUpdate model (what fields to update)

def update_contact(contact_id: str, updates: ContactUpdate):
    # TWO FUNCTION PARAMETERS:
    #
    # 1. contact_id: str
    #    - From URL path /contacts/{contact_id}
    #    - Tells us WHICH contact to update
    #
    # 2. updates: ContactUpdate
    #    - From request BODY (JSON payload)
    #    - Tells us WHAT to update
    #    - FastAPI automatically parses JSON → ContactUpdate object
    #    - User can send just {"email": "new@email.com"} (partial update!)

    """Update an existing contact. Supports partial updates (send only fields you want to change)."""

    # ========================================
    # STEP 1: Find the contact to update
    # ========================================
    for contact in contacts_db:
        # Loop through all contacts
        # POWER PLATFORM ANALOGY: Like "Get items" then "Apply to each" in Power Automate

        if contact["id"] == contact_id:
            # Found the contact with matching ID

            # ========================================
            # STEP 2: Extract ONLY the fields user wants to update
            # ========================================
            update_data = updates.model_dump(exclude_unset=True)
            # THIS IS THE MAGIC LINE FOR PARTIAL UPDATES!
            #
            # .model_dump() converts Pydantic model → dictionary
            #
            # exclude_unset=True = THE KEY TO PARTIAL UPDATES
            #   - "unset" = fields the user didn't provide in their request
            #   - "exclude" = don't include them in the dictionary
            #
            # Example:
            #   User sends: {"email": "new@email.com"}
            #   WITHOUT exclude_unset=True:
            #     {"name": None, "email": "new@email.com", "phone": None, "notes": None}
            #   WITH exclude_unset=True:
            #     {"email": "new@email.com"}  ← Only the field user sent!
            #
            # POWER PLATFORM ANALOGY:
            #   Like Patch(Contacts, record, {Email: "new@email.com"})
            #   Only updates Email field, leaves other fields unchanged


            # ========================================
            # STEP 3: Update the contact with new values
            # ========================================
            contact.update(update_data)
            # .update() is a Python dictionary method
            # It MERGES update_data INTO contact
            # Only updates keys that exist in update_data
            #
            # Example:
            #   contact before: {"id": "123", "name": "John", "email": "old@email.com", "phone": "555-0000"}
            #   update_data:    {"email": "new@email.com"}
            #   contact after:  {"id": "123", "name": "John", "email": "new@email.com", "phone": "555-0000"}
            #                                                          ↑ changed        ↑ unchanged
            #
            # POWER PLATFORM ANALOGY: Like merging two JSON objects in Power Automate


            # ========================================
            # STEP 4: Return the updated contact
            # ========================================
            return contact
            # Return the full contact with updated values
            # FastAPI converts → JSON with HTTP 200 (OK)


    # ========================================
    # STEP 5: Contact not found (error handling)
    # ========================================
    # If the for loop completes without finding the contact:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Contact with id {contact_id} not found"
    )
    # Return 404 error
    # POWER PLATFORM ANALOGY: Like checking if Update action succeeded in Power Automate


# ========================================
# ENDPOINT 5: DELETE CONTACT (DELETE)
# ========================================
# POWER PLATFORM ANALOGY:
# - Like "Delete a record" action in Power Automate
# - Or Remove() function in Power Apps to delete from Dataverse

@app.delete("/contacts/{contact_id}")
# @app.delete() = DELETE request (removing data)
# DELETE = "Remove this resource"
# {contact_id} = path parameter - which contact to delete

# NO response_model specified
# We return a simple message, not a ContactResponse object
# FastAPI allows returning plain dictionaries or strings

def delete_contact(contact_id: str):
    # FUNCTION PARAMETER:
    # contact_id: str - from URL path, identifies which contact to delete

    """Delete a contact permanently. Returns confirmation message."""

    # ========================================
    # STEP 1: Find the contact AND its index
    # ========================================
    for index, contact in enumerate(contacts_db):
        # enumerate() is a Python built-in function
        # It gives you BOTH the index AND the item while looping
        #
        # Normal loop:     for contact in contacts_db:
        #   - You get: contact (the item)
        #   - You DON'T get: which position it's at
        #
        # With enumerate: for index, contact in enumerate(contacts_db):
        #   - You get: index (0, 1, 2, ...) AND contact (the item)
        #
        # Example:
        #   contacts_db = [{"id": "a", ...}, {"id": "b", ...}, {"id": "c", ...}]
        #   Loop 1: index=0, contact={"id": "a", ...}
        #   Loop 2: index=1, contact={"id": "b", ...}
        #   Loop 3: index=2, contact={"id": "c", ...}
        #
        # WHY WE NEED INDEX:
        # To remove an item from a list, we need its position (index)
        # POWER PLATFORM ANALOGY: Like getting both item and index in Power Automate's Apply to each

        if contact["id"] == contact_id:
            # Found the contact to delete!

            # ========================================
            # STEP 2: Remove from database
            # ========================================
            contacts_db.pop(index)
            # .pop(index) is a Python list method
            # Removes and returns the item at the specified index
            #
            # Example:
            #   Before: contacts_db = [contact_a, contact_b, contact_c]
            #   contacts_db.pop(1)  ← remove item at index 1
            #   After:  contacts_db = [contact_a, contact_c]
            #
            # Alternative methods:
            #   - contacts_db.remove(contact) ← remove by value
            #   - del contacts_db[index] ← delete by index
            # We use .pop() because we have the index from enumerate()
            #
            # POWER PLATFORM ANALOGY:
            #   Like RemoveIf() in Power Apps or Remove() from Collection


            # ========================================
            # STEP 3: Return success message
            # ========================================
            return {"message": "Contact deleted"}
            # Return a plain Python dictionary
            # FastAPI automatically converts → JSON: {"message": "Contact deleted"}
            # HTTP status code = 200 (OK) by default
            #
            # NOTE: Some APIs return 204 (No Content) for DELETE
            # 204 = success but no response body
            # We're using 200 with a confirmation message (more user-friendly)
            #
            # POWER PLATFORM ANALOGY: Like returning success message in HTTP Response


    # ========================================
    # STEP 4: Contact not found (error handling)
    # ========================================
    # If the for loop completes without finding the contact:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Contact with id {contact_id} not found"
    )
    # Return 404 error - can't delete something that doesn't exist!
    # POWER PLATFORM ANALOGY: Like error handling in Power Automate when record not found


# ============================================
# END OF API ENDPOINTS
# ============================================
# That's it! We've implemented a complete REST API with:
# - CREATE (POST)
# - READ (GET single & list)
# - UPDATE (PUT with partial updates)
# - DELETE
#
# This is called CRUD (Create, Read, Update, Delete)
# POWER PLATFORM ANALOGY: Like having all Dataverse operations available via HTTP
#
# FastAPI automatically provides:
# ✓ API documentation at http://localhost:8000/docs
# ✓ JSON parsing and validation
# ✓ Type checking
# ✓ Error handling
# ✓ OpenAPI schema generation
