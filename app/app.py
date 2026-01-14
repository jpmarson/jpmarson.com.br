import os
import sqlite3
from datetime import datetime
from pathlib import Path

from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "blog.db"
UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["ADMIN_USERNAME"] = os.environ.get("ADMIN_USERNAME", "admin")
app.config["ADMIN_PASSWORD_HASH"] = os.environ.get(
    "ADMIN_PASSWORD_HASH", generate_password_hash("admin")
)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                image_filename TEXT,
                created_at TEXT NOT NULL,
                views INTEGER NOT NULL DEFAULT 0,
                likes INTEGER NOT NULL DEFAULT 0
            )
            """
        )


UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
init_db()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def requires_auth(view):
    def wrapped(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.type != "basic":
            return _auth_challenge()
        if auth.username != app.config["ADMIN_USERNAME"]:
            return _auth_challenge()
        if not check_password_hash(app.config["ADMIN_PASSWORD_HASH"], auth.password):
            return _auth_challenge()
        return view(*args, **kwargs)

    wrapped.__name__ = view.__name__
    return wrapped


def _auth_challenge():
    return (
        "Authentication required",
        401,
        {"WWW-Authenticate": 'Basic realm="Admin"'},
    )


@app.route("/")
def index():
    with get_db() as conn:
        posts = conn.execute(
            "SELECT id, title, body, image_filename, created_at, views, likes FROM posts ORDER BY id DESC"
        ).fetchall()
    return render_template("index.html", posts=posts)


@app.route("/post/<int:post_id>")
def post_detail(post_id):
    with get_db() as conn:
        conn.execute("UPDATE posts SET views = views + 1 WHERE id = ?", (post_id,))
        post = conn.execute(
            "SELECT id, title, body, image_filename, created_at, views, likes FROM posts WHERE id = ?",
            (post_id,),
        ).fetchone()
    if post is None:
        abort(404)
    return render_template("post.html", post=post)


@app.route("/post/<int:post_id>/like", methods=["POST"])
def like_post(post_id):
    with get_db() as conn:
        conn.execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))
        row = conn.execute(
            "SELECT likes FROM posts WHERE id = ?", (post_id,)
        ).fetchone()
    if row is None:
        abort(404)
    return jsonify({"likes": row[0]})


@app.route("/admin/new", methods=["GET", "POST"])
@requires_auth
def new_post():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        image = request.files.get("image")

        if not title or not body:
            return render_template(
                "admin_new.html",
                error="Title and body are required.",
                title=title,
                body=body,
            )

        image_filename = None
        if image and image.filename:
            if not allowed_file(image.filename):
                return render_template(
                    "admin_new.html",
                    error="Unsupported image format.",
                    title=title,
                    body=body,
                )
            safe_name = secure_filename(image.filename)
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
            image_filename = f"{timestamp}_{safe_name}"
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))

        with get_db() as conn:
            conn.execute(
                """
                INSERT INTO posts (title, body, image_filename, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (title, body, image_filename, datetime.utcnow().isoformat()),
            )

        return redirect(url_for("index"))

    return render_template("admin_new.html")


if __name__ == "__main__":
    app.run(debug=True)
