# Django Blog

A Django blog application with user registration, post creation, category and
status filters, and threaded comments. Signed-in users can comment on a post and
reply to comments at any nesting level.

## Requirements

- Python 3.12–3.15 ([supported by Django 6.1](https://docs.djangoproject.com/en/6.1/faq/install/))
- PostgreSQL

Python dependencies are listed in `requirements.txt`. Flake8 development tooling
is listed in `requirements-dev.txt`.

## Local setup

1. Clone the repository and change into its directory:

   ```bash
   git clone https://github.com/tawhiduradnan/django-blogsite-backend.git
   cd django-blogsite-backend
   ```
2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows, activate it with `.venv\Scripts\activate`.

3. Install the application and development dependencies:

   ```bash
   python -m pip install -r requirements-dev.txt
   ```

4. Create a PostgreSQL database named `blog`, or choose another name and update
   `DATABASES` in `blog/settings.py`. Configure its database user, password,
   host, and port there as well.
5. Apply database migrations and create an administrator account:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

Open <http://127.0.0.1:8000/> in a browser. The Django admin is at
<http://127.0.0.1:8000/admin/>.

## Main routes

| URL | Purpose | Sign-in required |
| --- | --- | --- |
| `/` | Browse and filter posts | No |
| `/post/<id>/` | View a post, comments, and reply thread | No |
| `/create_post/` | Create a post | Yes |
| `/register/` | Register an account | No |
| `/login/` | Sign in | No |
| `/logout/` | Sign out | Yes |

## Features

- Register, sign in, and sign out with Django authentication.
- Create posts and assign them to categories.
- Filter the post list by search text, category, and status.
- Add comments to a post and reply recursively to any comment in that post's
  thread.
- Manage posts, categories, and comments through Django admin.

## Project layout

```text
accounts/       Registration and account URLs
blog/           Django project settings and root URLs
posts/          Post and comment models, forms, views, and URLs
static/         Site CSS
templates/      Page templates, including recursive comment rendering
manage.py       Django management entry point
```

## Development checks

Run Django's system check and test suite with:

```bash
python manage.py check
python manage.py test
```

Run Flake8 against the Python code with:

```bash
python -m flake8
```

Flake8 configuration is in `.flake8`. It checks Python style and common code
issues; it does not validate Django templates or CSS.

## Configuration and security

The current database connection and Django `SECRET_KEY` are configured in
`blog/settings.py`. Use local development values for local work. Before
deploying, load secrets from environment variables or a secret manager, set
`DEBUG` to `False`, configure `ALLOWED_HOSTS`, and follow Django's deployment
checklist. Never commit real passwords, secret keys, or production credentials.

## License

No license is currently specified. Add a `LICENSE` file before redistributing
this project if you want to grant others explicit reuse rights.
