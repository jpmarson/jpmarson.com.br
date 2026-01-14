# JP Marson Blog

A simple personal site with a blog built in Flask.

## Features
- Posts with text and optional images
- View counting per post
- Like button per post

## Setup
1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install flask
```

2. Run the app:

```bash
python app/app.py
```

3. Open http://127.0.0.1:5000

## Creating posts
Visit http://127.0.0.1:5000/admin/new to create a new post.

### Admin authentication
Basic auth protects the admin page. Set credentials with environment variables:

```bash
export ADMIN_USERNAME="your-user"
export ADMIN_PASSWORD_HASH="$(python -c 'from werkzeug.security import generate_password_hash; print(generate_password_hash(\"your-pass\"))')"
```

Defaults are `admin` / `admin` if you do not set them.

Images are stored under `app/static/uploads`.
