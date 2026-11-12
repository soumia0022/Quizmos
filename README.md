# Quizmos

A real-time classroom polling web app. Lecturers create polls and run them live, and students join with a session code or QR code and answer from their own devices. Results update instantly.

Built as a 7-person group project for the Software Engineering Group (SEG) module at King's College London (Jan–Apr 2025). The project received 100% in the assessment.


### 🔗 [Live demo](https://quizmos.onrender.com/)
---

## Features

**For lecturers**
- Create, edit, archive and delete polls and questions.
- Question types: multiple choice, matching, drop-down, word cloud, free text and coding questions (with a code editor).
- Add images, audio, video and YouTube links to questions, with link validation.
- Run polls live: lock or unlock the poll, move between questions, and reveal the correct answer on every student's screen at once.
- Analytics with charts, word clouds, filtering and sorting, plus CSV export of responses.

**For students**
- Join a live poll with a session code or by scanning a QR code; guest access is supported.
- Answers are submitted and shown in real time over WebSockets.
- Partially correct answers are recognised for multiple choice and matching questions.

**Across the platform**
- Role-based access control: students, lecturers and guests can only reach their own pages.
- Custom 403, 404 and 500 error pages handled by middleware.
- A profanity filter on submitted responses.
- Password reset by email, profile pictures and text-to-speech for accessibility.

---

## Tech stack

| Area | Technologies |
|---|---|
| Backend | Python, Django 5, Django REST Framework |
| Real time | Django Channels (WebSockets), Redis, Daphne |
| Frontend | JavaScript, HTML, CSS, CodeMirror |
| Data & analytics | SQLite / PostgreSQL, Matplotlib, WordCloud |
| Testing | Django test framework, pytest, Selenium, Jest, coverage |
| DevOps | GitHub Actions (CI), AWS EC2, Nginx, Gunicorn |

---

## Project structure

| App | Responsibility |
|---|---|
| `user_management` | Student, lecturer and guest accounts, authentication, profiles |
| `poll_management` | Creating and running polls; WebSocket consumers for live sessions |
| `question_management` | Creating, editing, searching and sorting questions |
| `response_management` | Collecting and storing student answers in real time |
| `analytics` | Charts, word clouds and CSV export of results |
| `system_components` | Shared templates, middleware and error pages |

---

## My contribution

I made 300+ commits across the project, mainly in these areas:

- **Real-time polling:** refactored the poll WebSocket consumer into separate connection, message-handling and database layers; tracked lecturer connection and disconnection; revealed correct answers live on student screens.
- **Access control and security:** login decorators and permission checks so students, lecturers and guests can only reach the pages meant for them; middleware-based 403/404/500 error pages; fixes to the profanity-filter middleware; validation of YouTube links and question inputs.
- **Poll features:** archiving and unarchiving polls, viewing responses by session code, partially correct scoring for multiple choice and matching questions, coding and drop-down question displays.
- **Testing:** wrote and fixed tests for views, consumers and the profanity filter, and increased overall test coverage.
- **Code quality:** split large inline scripts into reusable JavaScript modules, converted views to class-based views and removed duplicated code.
- **Data housekeeping:** a management command to clean up expired guest users.
- **Secrets clean-up (after the module):** found credentials hard-coded in the settings file (Django secret key, email and database passwords). I moved all configuration to environment variables (`django-environ` with a `.env.example`), turned `DEBUG` off by default, removed the credentials from the full Git history with `git filter-repo`, and arranged for the exposed credentials to be revoked.

---

## Getting started

### Prerequisites
- Python 3.12
- Redis (running on `localhost:6379`)
- Node.js 18+ (only needed for the JavaScript tests)

### Setup

```bash
git clone https://github.com/soumia0022/quizmos.git
cd quizmos

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # then set DJANGO_SECRET_KEY (see the comment in the file)

python manage.py migrate
python manage.py seed           # optional: adds demo users, polls and questions
python manage.py runserver
```

Open http://127.0.0.1:8000.

### Configuration

All secrets and environment-specific settings are read from environment variables or a local `.env` file, which is never committed. See [`.env.example`](.env.example) for the full list: secret key, debug mode, allowed hosts, an optional PostgreSQL `DATABASE_URL`, Redis and SMTP email settings. Without SMTP settings, emails such as password resets are printed to the terminal.

### Demo accounts (created by `seed`)

| Role | Username | Password |
|---|---|---|
| Lecturer | `charlie` | `Password123` |
| Student | `johndoe` | `Password123` |

These are local test accounts only.

---

## Running tests

```bash
python manage.py test           # Django tests
npm install && npm test         # JavaScript (Jest) tests
```

Tests also run automatically on every push through GitHub Actions.

---

## Team

Amina Ali · Rashida Begum · **Soumia Bekhli** · Alishba Faisal · Leyli Jalilova · Eeshal Malik · Marium Rukiya

This repository is a copy of the team's original repository, with the full commit history kept.

## References

- [Django Channels tutorial](https://channels.readthedocs.io/en/stable/tutorial/part_1.html) was used to set up the real-time consumers.
