# Sponsor Portfolio Management Portal

This repository contains a complete sponsor and client portfolio management portal built with FastAPI and a responsive single-page UI.

## Features

- Sponsor and client CRUD operations
- Search across sponsors and clients
- Filter sponsors and clients by status and query parameters
- Sponsor-client relationship and client assignment support
- Login window for sponsors and clients with email/password authentication
- Dashboard summary endpoint for analytics and portfolio metrics
- Responsive UI for desktop and mobile
- Attractive hero layout with portfolio-style content
- Local SQLite storage with `portal.db`

## Run Locally

1. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   uvicorn app:app --reload
   ```
3. Open the portal in your browser:
   ```text
   http://127.0.0.1:8000/
   ```
4. Visit API documentation at:
   ```text
   http://127.0.0.1:8000/docs
   ```

## File Structure

- `app.py` — FastAPI backend
- `database.py` — SQLite and SQLAlchemy setup
- `models.py` — Sponsor and client models
- `schemas.py` — Request/response validation
- `static/index.html` — frontend UI
- `static/styles.css` — styling and layout
- `static/app.js` — portal interactions
- `static/images/portal-illustration.svg` — hero illustration

## Notes

- Data is stored in `portal.db` in the repository root.
- The backend now supports sponsor-client assignment and relationship mapping.
- If upgrading from an older version, delete `portal.db` before restarting to regenerate the schema.
- Update sponsors and clients directly from the portal UI.
- Search is available for sponsors and clients to quickly filter records.
