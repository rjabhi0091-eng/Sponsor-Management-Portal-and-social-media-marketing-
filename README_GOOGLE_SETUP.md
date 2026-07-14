Google API Integration Setup (Quick Start)

Overview
- This guide shows how to enable Google APIs (Sheets, Drive, Forms, Docs, Analytics) and run the example FastAPI integration provided in `google_integration.py`.

Step 1 — Create a Google Cloud Project and OAuth credentials
1. Go to https://console.cloud.google.com and create or select a project.
2. Enable these APIs in the API Library:
   - Google Sheets API
   - Google Drive API
   - Google Forms API (optional and may require additional access)
   - Google Docs API
   - Google Analytics Data API (for GA4 reporting)
3. Open "Credentials" → "OAuth consent screen" and configure your app (external or internal). Add your domain or `http://localhost:8000` for testing.
4. Create OAuth 2.0 Client ID (Web application). Add an authorized redirect URI:
   - `http://localhost:8000/google/oauth2callback`
5. Download the JSON credentials and save as `client_secret.json` in the project root (or set `GOOGLE_CLIENT_SECRETS` environment variable to its path).

Step 2 — Configure environment variables
- Create a `.env` file in the project root with the following keys (adjust names as needed):

```
GOOGLE_CLIENT_SECRETS=client_secret.json
GOOGLE_OAUTH_REDIRECT=http://localhost:8000/google/oauth2callback
GOOGLE_TOKEN_FILE=google_tokens.json  # optional fallback
GOOGLE_DB_URL=sqlite:///google_tokens.db
```

Step 3 — Install dependencies
Run in your project environment:

```bash
pip install -r requirements.txt
```

Step 4 — Run the example server

```bash
uvicorn google_integration:app --reload
```

Step 5 — Authorize the app
1. Open `http://localhost:8000/google/login` in your browser.
2. Complete Google sign-in and consent. The callback will save tokens to `google_tokens.db` using SQLite.

Step 6 — Use the endpoints
- Read sheet values as JSON:
  - `GET /google/sheets/{sheetId}`
  - Optional query param `?range=A1:C200`
- Export sheet as `.xlsx`:
  - `GET /google/sheets/{sheetId}/export.xlsx`
- Fetch Forms responses:
  - `GET /google/forms/{formId}`
- Export Docs to PDF:
  - `GET /google/docs/{docId}/export.pdf`
- Run GA4 Analytics report (POST JSON):
  - `POST /google/analytics` with body `{"propertyId":"<GA4_PROPERTY_ID>", "request": { ... runReport body ... }}`
- Combined export (sheet + summary):
  - `GET /google/export/combined/{sheetId}`

Security notes
- Tokens are stored locally in an SQLite DB for convenience; for production, use an encrypted secrets backend and restrict access.
- Limit scopes to the minimum required for each feature.

Next steps (optional)
- Provide a secure admin UI to refresh tokens, view connected account, and revoke access.
- Add background refresh of tokens and per-user token storage.
