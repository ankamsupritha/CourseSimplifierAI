from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename
import sqlite3
import os
from services.pdf_service import extract_text
from services.ai_service import simplify_course
from services.agent_service import chat_with_agent

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
    c.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        filename TEXT,
        notes TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute(
        "SELECT COUNT(*) FROM history WHERE username=?",
        (session["user"],)
    )
    documents = c.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        username=session["user"],
        documents=documents
    )


@app.route("/upload", methods=["POST"])
def upload():

    if "user" not in session:
        return redirect("/")

    file = request.files["pdf"]

    if not file.filename:
        flash("Please select a file")
        return redirect("/dashboard")

    filename = secure_filename(file.filename)

    filepath = os.path.join(
    app.config["UPLOAD_FOLDER"],
    filename
)

    file.save(filepath)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute(
        """
        INSERT INTO history(username, filename)
        VALUES(?,?)
        """,
        (session["user"], file.filename)
    )

    conn.commit()
    conn.close()

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

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    full_notes = result["summary"]

    c.execute("""
    UPDATE history
    SET notes=?
    WHERE id=(
    SELECT MAX(id)
    FROM history
    WHERE username=?
    )
    """,(
    full_notes,
    session["user"]
    ))

    conn.commit()
    conn.close()

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

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute("""
        SELECT id, filename, uploaded_at
        FROM history
        WHERE username=?
        ORDER BY uploaded_at DESC
    """, (session["user"],))

    history_data = c.fetchall()

    conn.close()

    return render_template(
        "history.html",
        history_data=history_data
    )


@app.route("/view/<int:id>")
def view_notes(id):

    if "user" not in session:
        return redirect("/")

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute("""
        SELECT filename, notes
        FROM history
        WHERE id=? AND username=?
    """,(id,session["user"]))

    data=c.fetchone()

    conn.close()

    if not data:
        return redirect("/history")

    return render_template(
        "result.html",
        filename=data[0],
        result={"summary":data[1]}
    )


@app.route("/download/<int:id>")
def download_notes(id):

    if "user" not in session:
        return redirect("/")

    conn=sqlite3.connect(DATABASE)
    c=conn.cursor()

    c.execute("""
        SELECT filename,notes
        FROM history
        WHERE id=? AND username=?
    """,(id,session["user"]))

    data=c.fetchone()

    conn.close()

    if not data:
        return redirect("/history")

    from flask import Response

    return Response(
        data[1],
        mimetype="text/plain",
        headers={
            "Content-Disposition":
            f"attachment; filename={data[0]}_SmartNotes.txt"
        }
    )


# --------------------------
# ABOUT
# --------------------------

@app.route("/about")
def about():

    return render_template("about.html")


# --------------------------
# AGENT CHAT (UI)
# --------------------------

@app.route("/agent")
def agent():

    if "user" not in session:
        return redirect("/")

    return render_template("agent.html", username=session["user"])


# --------------------------
# AGENT CHAT (API)
# --------------------------

@app.route("/api/agent/chat", methods=["POST"])
def api_agent_chat():
    """
    REST endpoint consumed by the UI and by the IBM watsonx Orchestrate skill.

    Request JSON:
        { "message": "...", "history": [{"role": "user"|"assistant", "text": "..."}] }

    Response JSON:
        { "reply": "...", "history": [...] }
    """
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "Missing 'message' field"}), 400

    history = data.get("history") or []

    try:
        reply = chat_with_agent(history, user_message)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Append the new exchange to history
    updated_history = history + [
        {"role": "user", "text": user_message},
        {"role": "assistant", "text": reply},
    ]

    return jsonify({"reply": reply, "history": updated_history})


@app.route("/api/agent/simplify", methods=["POST"])
def api_agent_simplify():
    """
    REST endpoint that runs the full structured simplification pipeline.
    Consumed by the IBM watsonx Orchestrate skill.

    Request JSON:
        { "text": "..." }

    Response JSON:
        { "summary": "..." }
    """
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "Missing 'text' field"}), 400

    try:
        result = simplify_course(text)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(result)


# --------------------------
# LOGOUT
# --------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":

    app.run(debug=True)