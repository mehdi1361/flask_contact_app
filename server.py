from flask import Flask, jsonify, request, abort, render_template, redirect, url_for
from models import Contact, repo, PhoneNumber, Email

app = Flask(__name__)


def serialize_contact(contact: Contact):
    return {
        "id": contact.contact_id,
        "name": contact.name,
        "email": str(contact.email),
        "phone": str(contact.phone),
    }


@app.get("/")
def index():
    return render_template(
        "index.html",
    )

@app.get("/contacts")
def list_contacts():
    q = request.args.get("q")

    if q:
        contacts = repo.search(q)
    else:
        contacts = repo.list_active()

    # تبدیل Contact → چیزی که template بفهمه
    view_contacts = [
        {
            "id": c.contact_id,
            "first": c.name.split()[0],
            "last": " ".join(c.name.split()[1:]),
            "phone": str(c.phone),
            "email": str(c.email),
        }
        for c in contacts
    ]

    return render_template(
        "contact.html",
        contacts=view_contacts,
    )


@app.route("/contacts/<int:contact_id>/edit", methods=["GET", "POST"])
def edit_contact(contact_id):
    contact = repo.get_by_id(contact_id)
    if not contact:
        abort(404)

    if request.method == "POST":
        # آپدیت ساده برای دمو
        first = request.form.get("first", "").strip()
        last = request.form.get("last", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()

        if not first or not email:
            abort(400)

        contact.name = f"{first} {last}".strip()
        contact.phone = PhoneNumber(phone)
        contact.email = Email(email)

        repo.save(contact)
        return redirect(url_for("list_contacts"))

    # GET → رندر فرم
    first, *rest = contact.name.split()
    last = " ".join(rest)

    return render_template(
        "contact_edit.html",
        contact={
            "id": contact.contact_id,
            "first": first,
            "last": last,
            "phone": str(contact.phone),
            "email": str(contact.email),
        },
    )

@app.route("/contacts/new", methods=["GET", "POST"])
def new_contact():
    if request.method == "POST":
        first = request.form.get("first", "").strip()
        last = request.form.get("last", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()

        if not first or not email:
            abort(400)

        new_id = max(repo._contacts.keys(), default=0) + 1

        contact = Contact(
            contact_id=new_id,
            name=f"{first} {last}".strip(),
            phone=PhoneNumber(phone),
            email=Email(email),
        )

        repo.save(contact)
        return redirect(url_for("list_contacts"))

    return render_template("contact_new.html")

@app.get("/contacts/<int:contact_id>")
def view_contact(contact_id):
    contact = repo.get_by_id(contact_id)
    if not contact:
        abort(404)

    first, *rest = contact.name.split()
    last = " ".join(rest)

    return render_template(
        "contact_view.html",
        contact={
            "id": contact.contact_id,
            "first": first,
            "last": last,
            "phone": str(contact.phone),
            "email": str(contact.email),
        },
    )
