# CASTER Learning Technologies

**Learn. Create. Excel Everywhere.**

A learning technology platform for Junior Achievement Nigeria, built with Django, Tailwind CSS, and PostgreSQL.

## Stack

- **Django 6** — apps organized under `apps/`, class-based views, `forms.py` for validation
- **Tailwind CSS v4** via [django-tailwind](https://github.com/timonweb/django-tailwind), using the **standalone CLI binary** (no Node.js/npm required — the CLI is installed and managed through the `pytailwindcss` pip package)
- **PostgreSQL** as the primary database, with environment-based settings (`django-environ`)
- **Whitenoise** for static file serving

### Why django-tailwind + the standalone CLI?

`django-tailwind` wires Tailwind's build step into Django's own management commands
(`manage.py tailwind build`/`start`) and ships a `{% tailwind_css %}` template tag, so
templates don't need a separate frontend build pipeline to reason about. The **standalone
CLI** variant downloads a self-contained `tailwindcss` binary instead of requiring Node.js
and `node_modules` — fewer moving parts to install on a new machine, no JS toolchain to
maintain, and no npm dependency drift. If you later need Tailwind plugins that only ship as
npm packages, `django-tailwind` also supports the full Node-based template.

## Project layout

```
caster/
├── config/                 # Django project settings, root urls
├── apps/
│   └── marketing/          # Phase 1: public landing site + waitlist
├── theme/                  # django-tailwind app (Tailwind source + compiled CSS)
├── templates/              # Project-level templates (base.html, includes/, marketing/)
├── static/                 # Project-level static assets (images, etc.)
├── requirements.txt
├── .env.example
└── manage.py
```

Phase 2 will add `apps/accounts`, `apps/study`, and `apps/assessments` for the learning
platform (custom user model, study guides, quizzes, progress tracking).

## Setup

### 1. Clone and create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and set `DJANGO_SECRET_KEY`. By default it points at PostgreSQL via
`DATABASE_URL`. To run the landing page without installing Postgres locally, you can
instead set:

```
DATABASE_URL=sqlite:///db.sqlite3
```

### 3. Set up PostgreSQL (recommended)

```sql
CREATE DATABASE caster;
CREATE USER caster WITH PASSWORD 'caster';
GRANT ALL PRIVILEGES ON DATABASE caster TO caster;
```

Make sure `DATABASE_URL` in `.env` matches these credentials.

### 4. Run migrations

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Build Tailwind CSS

First-time setup downloads the standalone Tailwind CLI binary:

```bash
python manage.py tailwind install
```

Build once:

```bash
python manage.py tailwind build
```

Or watch for changes while developing:

```bash
python manage.py tailwind start
```

### 6. Run the dev server

In a second terminal (while `tailwind start` runs in the first, if you want live CSS
rebuilds):

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

## Admin

Visit `/admin/` and log in with the superuser you created to view waitlist signups
(**Marketing → Waitlist signups**).

## Environment variables

| Variable | Description | Default |
|---|---|---|
| `DEBUG` | Django debug mode | `False` |
| `DJANGO_SECRET_KEY` | Django secret key | — |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `DATABASE_URL` | Database connection URL | `postgres://caster:caster@localhost:5432/caster` |
| `DJANGO_EMAIL_BACKEND` | Email backend | console backend |
