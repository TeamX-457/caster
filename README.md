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
│   ├── marketing/          # Phase 1: public landing site + waitlist
│   ├── accounts/           # Phase 2: custom User (student/teacher/school_admin), School
│   ├── study/              # Phase 2: StudyGuide, LearningActivity, StudentProgress
│   └── assessments/        # Phase 2: Assessment, Question, Choice, AssessmentAttempt
├── theme/                  # django-tailwind app (Tailwind source + compiled CSS)
├── templates/              # Project-level templates (base.html, includes/, per-app dirs)
├── static/                 # Project-level static assets (images, etc.)
├── requirements.txt
├── .env.example
└── manage.py
```

## The learning platform (Phase 2)

- **Custom user model** (`apps.accounts.User`, `AUTH_USER_MODEL`) with a `role` field
  (`student` / `teacher` / `school_admin`) and a `school` FK. `Teacher` and `Student` are
  one-to-one profile models holding role-specific fields.
- **Roles and how accounts are created:**
  - *School admin* — registers at `/accounts/signup/school/`, which creates both the
    `School` and the admin's `User` in one step.
  - *Teacher* — added by a school admin from their dashboard (`/accounts/teachers/add/`);
    there's no public teacher self-registration, since a school should control who can
    create content and see its students' data.
  - *Student* — registers at `/accounts/signup/student/`, selecting their school from a
    list of already-registered schools.
- **Dashboards** (`/accounts/dashboard/`) branch by role: students see assigned study
  guides with progress status and their assessment history; teachers see their study
  guides and their school's students; school admins see aggregate counts, their teacher
  roster, and their student roster.
- **Study guides**: a teacher creates a `StudyGuide` (subject/topic/title/content), can add
  `LearningActivity` entries to it, and assigns it to specific students — which creates a
  `StudentProgress` row per student. Opening the guide as a student advances its status
  `assigned → in_progress`; a "Mark as completed" button advances it to `completed`.
- **Assessments**: a teacher attaches an `Assessment` to a study guide and adds
  multiple-choice `Question`/`Choice` pairs one at a time. Students take the assessment;
  submitting grades it server-side and stores an `AssessmentAttempt` (score/total) plus a
  `StudentAnswer` per question, both shown in the student's assessment history.
- **No seed data**: the app ships with no fixtures and no demo accounts. Every school,
  teacher, student, study guide, and assessment is created through the real registration
  and content-management flows described above.

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
(**Marketing → Waitlist signups**) and all Phase 2 data (schools, users, study guides,
assessments, progress, and attempts).

## Trying out the learning platform

There's no seed data, so exercise the real flows:

1. Go to `/accounts/signup/school/` and register a school — you become its admin.
2. From your dashboard, use **+ Add teacher** to create a teacher account.
3. Log out, log in as the teacher, and create a study guide (**+ New study guide**).
4. Add an activity and an assessment (with questions/choices) to it.
5. Go to `/accounts/signup/student/` in a different browser/session and register a
   student, selecting the school from step 1.
6. Back as the teacher, open the study guide and **Assign to students**.
7. Log in as the student to see the assigned guide, mark it complete, and take the
   assessment — the score and history show up immediately on the student dashboard.

## Environment variables

| Variable | Description | Default |
|---|---|---|
| `DEBUG` | Django debug mode | `False` |
| `DJANGO_SECRET_KEY` | Django secret key | — |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `DATABASE_URL` | Database connection URL | `postgres://caster:caster@localhost:5432/caster` |
| `DJANGO_EMAIL_BACKEND` | Email backend | console backend |
