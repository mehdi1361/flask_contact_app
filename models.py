from flask import Flask, jsonify, request, abort

# ---------- Domain ----------

class Email:
    def __init__(self, value: str):
        if "@" not in value:
            raise ValueError("Invalid email")
        self.value = value

    def __str__(self):
        return self.value


class PhoneNumber:
    def __init__(self, value: str):
        if not value.isdigit():
            raise ValueError("Phone number must be digits")
        self.value = value

    def __str__(self):
        return self.value


class Contact:
    def __init__(self, contact_id: int, name: str, email: Email, phone: PhoneNumber):
        self.contact_id = contact_id
        self.name = name
        self.email = email
        self.phone = phone
        self._archived = False

    def archive(self):
        if self._archived:
            raise ValueError("Contact already archived")
        self._archived = True

    def is_active(self):
        return not self._archived


class ContactRepository:
    def get_by_id(self, contact_id: int):
        raise NotImplementedError

    def list_active(self):
        raise NotImplementedError

    def save(self, contact: Contact):
        raise NotImplementedError


class InMemoryContactRepository(ContactRepository):
    def __init__(self, contacts):
        self._contacts = {c.contact_id: c for c in contacts}

    def get_by_id(self, contact_id: int):
        return self._contacts.get(contact_id)

    def list_active(self):
        return [c for c in self._contacts.values() if c.is_active()]

    def search(self, query: str):
        q = query.lower()
        return [
            c for c in self.list_active()
            if q in c.name.lower() or q in str(c.email).lower()
        ]

    def save(self, contact: Contact):
        self._contacts[contact.contact_id] = contact


# ---------- Test Data ----------

repo = InMemoryContactRepository([
    Contact(1, "Ali Rezaei", Email("ali@example.com"), PhoneNumber("09120000001")),
    Contact(2, "Sara Mohammadi", Email("sara@example.com"), PhoneNumber("09120000002")),
    Contact(3, "Reza Karimi", Email("reza@example.com"), PhoneNumber("09120000003")),
])
