# Dorothea Reher – Django Portfolio

Personal portfolio website showcasing projects, a dev journal, skills, and a contact form.
Built with Django, served via Gunicorn and WhiteNoise, and deployed with Docker on Render.

**Live:** [dorothea-reher.com](https://www.dorothea-reher.com/)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Framework | Django 6 |
| Database | PostgreSQL (production) / SQLite (development) |
| Server | Gunicorn |
| Static files | WhiteNoise |
| Rich text | TinyMCE |
| i18n | django-modeltranslation (EN / DE / FR) |
| Error tracking | Sentry |
| Containerisation | Docker |
| Hosting | Render |

---

## Apps

| App | Purpose |
|---|---|
| `accounts` | Custom user model and profile |
| `doridoro` | Home, about, skills, and resume pages |
| `projects` | Portfolio project list and detail views |
| `journal` | Dev journal entries |
| `contact` | Public contact form with email notification |
| `core` | Shared templates, static files, and sitemap |

---

## Versions

### version-1 — currently deployed

Initial release of the portfolio, live at [dorothea-reher.com](https://www.dorothea-reher.com/).

### version-2 — current development branch

- Upgraded all packages to their latest versions, including Django 6
- Migrated to the production data structure
- Added management commands to seed the database with real content (see [Management Commands](#management-commands) below)

---

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Setup

```sh
# 1. Clone and enter the repository
git clone <repo-url>
cd django_portfolio

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate       # Linux / macOS
.venv\Scripts\activate          # Windows

# 3. Install dependencies (includes dev tools: black, flake8, ipython)
pip install ".[dev]"

# 4. Configure environment variables
cp .env.example .env
# Edit .env and fill in all required values

# 5. Apply migrations and start the server
python manage.py migrate
python manage.py runserver
```

### Environment Variables

See [.env.example](.env.example) for the full list. Key variables:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key (generate with `make secret_key`) |
| `DEBUG` | Set to `True` for local development |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames |
| `DB_NAME` / `DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT` | PostgreSQL credentials (only required when `DEBUG=False`) |
| `SENTRY_DSN` | Optional Sentry DSN for error tracking |
| `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` | Gmail SMTP credentials for the contact form |
| `CONTACT_EMAIL` | Recipient address for contact form notifications |
| `PROJECT_NAME` | Project name used in email subjects |

---

## Management Commands

The `data_create` command seeds a fresh database with all production content in the correct order.

```sh
python manage.py data_create
```

This single command runs the following sub-commands in sequence:

| Command | Creates |
|---|---|
| `createsuperuser` | Admin superuser |
| `profile_create` | Owner profile |
| `achievements_create` | Achievements |
| `degrees_create` | Degrees |
| `jobs_create` | Work experience |
| `languages_create` | Spoken languages |
| `social_media_create` | Social media links |
| `platform_create` | Link platforms |
| `links_create` | External links |
| `journals_create` | Journal entries |
| `skills_create` | Skills |
| `projects_create` | Projects |

---

## Deployment

The project is deployed on [Render](https://render.com/) via a `Dockerfile`.

### Steps

1. Create a **PostgreSQL** managed database on Render and note the connection details.
2. Create a new **Web Service** on Render, point it to this repository, and select *Docker* as the environment.
3. Add all required environment variables from the table above in the Render dashboard (`DEBUG=False`, production DB credentials, etc.).
4. Render builds the image from the [`Dockerfile`](Dockerfile) and starts the container.
5. After the first deploy, seed the database:

```sh
# via Render Shell in the dashboard
python manage.py data_create
```

### Useful Make targets

```sh
make server        # Run Django development server
make create_db     # Run makemigrations + migrate
make data          # Run data_create management command
make secret_key    # Generate a new SECRET_KEY
```
