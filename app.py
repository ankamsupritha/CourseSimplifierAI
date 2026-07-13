from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from services.pdf_service import extract_text
from services.ai_service import simplify_course

app = Flask(__name__)
app.secret_key = "learnease_secret_key"

DATABASE = "learnease.db"
UPLOAD_FOLDER="uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER

# --------------------------
# DATABASE
# --------------------------

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# --------------------------
# LOGIN
# --------------------------

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        c.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = c.fetchone()

        conn.close()

        if user:

            session["user"] = user[1]
            return redirect("/dashboard")

        flash("Invalid Email or Password")

    return render_template("login.html")


# --------------------------
# REGISTER
# --------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        try:

            c.execute(
                "INSERT INTO users(fullname,email,password) VALUES(?,?,?)",
                (fullname, email, password)
            )

            conn.commit()

            flash("Registration Successful")

            return redirect("/")

        except:

            flash("Email already exists")

        conn.close()

    return render_template("register.html")


# --------------------------
# DASHBOARD
# --------------------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect("/")

    return render_template(
        "dashboard.html",
        username=session["user"]
    )


@app.route("/upload", methods=["POST"])
def upload():

    if "user" not in session:
        return redirect("/")

    file = request.files["pdf"]

    if file.filename == "":
        flash("Please select a PDF")
        return redirect("/dashboard")

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    # Save ONLY filename in session
    session["pdf_name"] = file.filename

    return redirect(url_for("preview"))


@app.route("/preview")
def preview():

    if "pdf_name" not in session:
        return redirect("/dashboard")

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        session["pdf_name"]
    )

    extracted_text = extract_text(filepath)

    result = simplify_course(extracted_text)

    return render_template(
        "result.html",
        filename=session["pdf_name"],
        result=result
    )


# --------------------------
# PROFILE
# --------------------------

@app.route("/profile")
def profile():

    if "user" not in session:

        return redirect("/")

    return render_template(
        "profile.html",
        username=session["user"]
    )


# --------------------------
# HISTORY
# --------------------------

@app.route("/history")
def history():

    if "user" not in session:

        return redirect("/")

    return render_template("history.html")


# --------------------------
# ABOUT
# --------------------------

@app.route("/about")
def about():

    return render_template("about.html")


# --------------------------
# LOGOUT
# --------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":

    app.run(debug=True)