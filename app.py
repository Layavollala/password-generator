from flask import Flask, render_template, request, redirect, url_for, session
import secrets
import string
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me-to-a-secure-random-key")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template("home.html")


# -----------------------------
# ABOUT PAGE
# -----------------------------
@app.route("/about")
def about():
    return render_template("about.html")


# -----------------------------
# CONTACT PAGE
# -----------------------------
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not subject or not message:
            return render_template(
                "contact.html",
                error="All fields are required.",
                name=name,
                email=email,
                subject=subject,
                message=message
            )

        contact_message = {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
            "received_at": datetime.utcnow().isoformat() + "Z"
        }

        os.makedirs("data", exist_ok=True)
        with open("data/messages.jsonl", "a", encoding="utf-8") as file:
            file.write(json.dumps(contact_message, ensure_ascii=False) + "\n")

        return render_template(
            "contact.html",
            success="Your message has been sent successfully.",
            name="",
            email="",
            subject="",
            message=""
        )

    return render_template("contact.html")


@app.route("/admin/messages")
def admin_messages():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    messages = []
    filepath = "data/messages.jsonl"
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    messages.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    messages.sort(key=lambda item: item.get("received_at", ""), reverse=True)
    return render_template("admin_messages.html", messages=messages)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_messages"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_messages"))

        error = "Invalid username or password."

    return render_template("admin_login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("home"))


# -----------------------------
# PASSWORD GENERATOR
# -----------------------------
@app.route("/generator", methods=["GET", "POST"])
def generator():

    password = ""
    strength = ""

    if request.method == "POST":

        length = int(request.form.get("length"))

        # enforce minimum length on server-side as well
        if length < 6:
            return render_template(
                "generator.html",
                password="",
                strength="",
                error="Minimum length: 6 characters"
            )

        uppercase = request.form.get("uppercase")
        lowercase = request.form.get("lowercase")
        numbers = request.form.get("numbers")
        symbols = request.form.get("symbols")

        characters = ""

        if uppercase:
            characters += string.ascii_uppercase

        if lowercase:
            characters += string.ascii_lowercase

        if numbers:
            characters += string.digits

        if symbols:
            characters += string.punctuation

        if characters != "":

            password = "".join(
                secrets.choice(characters)
                for i in range(length)
            )

            score = 0

            if length >= 8:
                score += 1

            if uppercase:
                score += 1

            if lowercase:
                score += 1

            if numbers:
                score += 1

            if symbols:
                score += 1

            if score <= 2:
                strength = "Weak"

            elif score <= 4:
                strength = "Medium"

            else:
                strength = "Strong"

            save = request.form.get("save")

            if save:

                with open("passwords.txt", "a") as file:
                    file.write(password + "\n")

    return render_template(
        "generator.html",
        password=password,
        strength=strength
    )


# -----------------------------
# RUN APPLICATION
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)