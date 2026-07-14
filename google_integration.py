import os
import json
import io
from typing import Optional
from fastapi import FastAPI, APIRouter, Request, HTTPException, Body
from fastapi.responses import RedirectResponse, StreamingResponse, JSONResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request as GoogleRequest
import pandas as pd
from dotenv import load_dotenv

# SQLAlchemy for token storage
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Configuration - expects CLIENT_SECRETS_FILE (JSON from Google Cloud) and REDIRECT_URI
CLIENT_SECRETS_FILE = os.environ.get("GOOGLE_CLIENT_SECRETS", "client_secret.json")
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/forms.responses.readonly",
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/analytics.readonly",
]
DB_URL = os.environ.get("GOOGLE_DB_URL", "sqlite:///google_tokens.db")

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    token_json = Column(Text)

Base.metadata.create_all(bind=engine)

TOKEN_STORE = os.environ.get("GOOGLE_TOKEN_FILE", None)  # optional legacy file

router = APIRouter()


def save_tokens_db(creds: Credentials):
    data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    }
    session = SessionLocal()
    try:
        existing = session.query(Token).first()
        if existing:
            existing.token_json = json.dumps(data)
        else:
            t = Token(token_json=json.dumps(data))
            session.add(t)
        session.commit()
    finally:
        session.close()


def load_credentials_db() -> Optional[Credentials]:
    session = SessionLocal()
    try:
        existing = session.query(Token).first()
        if not existing:
            # try legacy file
            if TOKEN_STORE and os.path.exists(TOKEN_STORE):
                with open(TOKEN_STORE, "r") as f:
                    data = json.load(f)
            else:
                return None
        else:
            data = json.loads(existing.token_json)
    finally:
        session.close()

    creds = Credentials(
        token=data.get("token"),
        refresh_token=data.get("refresh_token"),
        token_uri=data.get("token_uri"),
        client_id=data.get("client_id"),
        client_secret=data.get("client_secret"),
        scopes=data.get("scopes"),
    )

    if not creds.valid and creds.refresh_token:
        try:
            creds.refresh(GoogleRequest())
            save_tokens_db(creds)
        except Exception:
            return creds

    return creds


@router.get("/login")
def google_login(request: Request):
    # Build OAuth flow and redirect to Google consent
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=os.environ.get("GOOGLE_OAUTH_REDIRECT", "http://localhost:8000/google/oauth2callback"),
    )
    auth_url, _ = flow.authorization_url(access_type="offline", include_granted_scopes="true")
    return RedirectResponse(auth_url)


@router.get("/oauth2callback")
async def google_oauth2callback(request: Request):
    state = request.query_params.get("state")
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=os.environ.get("GOOGLE_OAUTH_REDIRECT", "http://localhost:8000/google/oauth2callback"),
    )
    authorization_response = str(request.url)
    flow.fetch_token(authorization_response=authorization_response)
    creds = flow.credentials
    # save to DB
    save_tokens_db(creds)
    return RedirectResponse("/")


@router.get("/sheets/{sheet_id}")
def read_sheet(sheet_id: str, range: str = None):
    creds = load_credentials_db()
    if not creds:
        raise HTTPException(status_code=401, detail="Google credentials not configured. Call /google/login first.")
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    range_to_read = range or "A1:Z1000"
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_to_read).execute()
    values = result.get("values", [])
    return JSONResponse(content={"values": values})


@router.get("/sheets/{sheet_id}/export.xlsx")
def export_sheet_xlsx(sheet_id: str, range: str = None):
    creds = load_credentials_db()
    if not creds:
        raise HTTPException(status_code=401, detail="Google credentials not configured. Call /google/login first.")
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    range_to_read = range or "A1:Z1000"
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_to_read).execute()
    values = result.get("values", [])
    # Convert to DataFrame
    if not values:
        df = pd.DataFrame()
    else:
        df = pd.DataFrame(values[1:], columns=values[0]) if len(values) > 1 else pd.DataFrame(values)
    stream = io.BytesIO()
    with pd.ExcelWriter(stream, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    stream.seek(0)
    headers = {
        "Content-Disposition": f"attachment; filename=sheet_{sheet_id}.xlsx"
    }
    return StreamingResponse(stream, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)


@router.get("/forms/{form_id}")
def get_form_responses(form_id: str):
    creds = load_credentials_db()
    if not creds:
        raise HTTPException(status_code=401, detail="Google credentials not configured. Call /google/login first.")
    try:
        service = build("forms", "v1", credentials=creds)
        # The Forms API exposes responses under forms().responses().list
        resp = service.forms().responses().list(formId=form_id).execute()
        return JSONResponse(content=resp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/docs/{doc_id}/export.pdf")
def export_doc_pdf(doc_id: str):
    creds = load_credentials_db()
    if not creds:
        raise HTTPException(status_code=401, detail="Google credentials not configured. Call /google/login first.")
    drive = build("drive", "v3", credentials=creds)
    try:
        data = drive.files().export(fileId=doc_id, mimeType="application/pdf").execute()
        return StreamingResponse(io.BytesIO(data), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=doc_{doc_id}.pdf"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analytics")
def run_analytics_report(payload: dict = Body(...)):
    creds = load_credentials_db()
    if not creds:
        raise HTTPException(status_code=401, detail="Google credentials not configured. Call /google/login first.")
    property_id = payload.get("propertyId")
    if not property_id:
        raise HTTPException(status_code=400, detail="propertyId is required in the request body")
    request_body = payload.get("request", {})
    try:
        analytics = build("analyticsdata", "v1beta", credentials=creds)
        name = f"properties/{property_id}"
        resp = analytics.properties().runReport(name=name, body=request_body).execute()
        return JSONResponse(content=resp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export/combined/{sheet_id}")
def export_combined(sheet_id: str, range: str = None):
    creds = load_credentials_db()
    if not creds:
        raise HTTPException(status_code=401, detail="Google credentials not configured. Call /google/login first.")
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    range_to_read = range or "A1:Z1000"
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_to_read).execute()
    values = result.get("values", [])
    # Convert to DataFrame
    if not values:
        df = pd.DataFrame()
    else:
        df = pd.DataFrame(values[1:], columns=values[0]) if len(values) > 1 else pd.DataFrame(values)
    # Create summary sheet
    summary = pd.DataFrame({"metric": ["total_rows"], "value": [max(0, len(values)-1)]})
    stream = io.BytesIO()
    with pd.ExcelWriter(stream, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
        summary.to_excel(writer, index=False, sheet_name="Summary")
    stream.seek(0)
    headers = {
        "Content-Disposition": f"attachment; filename=combined_{sheet_id}.xlsx"
    }
    return StreamingResponse(stream, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)


if __name__ == "__main__":
    app = FastAPI()
    app.include_router(router, prefix="/google")
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
