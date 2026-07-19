import os
import smtplib
from email.message import EmailMessage

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import or_, text
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from googleapiclient.discovery import build

import models
import schemas
import google_integration
from database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

with engine.connect() as connection:
    def existing_columns(table_name: str):
        result = connection.execute(text(f"PRAGMA table_info({table_name})"))
        return [row[1] for row in result.fetchall()]

    if "sponsor_id" not in existing_columns("clients"):
        connection.execute(text("ALTER TABLE clients ADD COLUMN sponsor_id INTEGER"))
    if "password_hash" not in existing_columns("sponsors"):
        connection.execute(text("ALTER TABLE sponsors ADD COLUMN password_hash TEXT DEFAULT ''"))
    if "password_hash" not in existing_columns("clients"):
        connection.execute(text("ALTER TABLE clients ADD COLUMN password_hash TEXT DEFAULT ''"))

with SessionLocal() as db:
    existing_admin = db.query(models.Admin).filter(models.Admin.email == ADMIN_EMAIL).first()
    if not existing_admin:
        admin = models.Admin(username=ADMIN_USERNAME, email=ADMIN_EMAIL)
        admin.set_password(ADMIN_PASSWORD)
        db.add(admin)
        db.commit()

BASE_DIR = os.path.dirname(__file__)

app = FastAPI(
    title="Sponsor and Client Management Portal",
    description="Backend API and UI for managing sponsors and clients in a single portal.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"]
)

SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret-key-for-development-only")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
security = HTTPBearer()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("sub") is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")
app.include_router(google_integration.router, prefix="/google")


def append_to_google_sheet(values: list[str]):
    sheet_id = os.environ.get("GOOGLE_SHEET_ID") or os.environ.get("SPONSOR_PORTAL_SHEET_ID")
    if not sheet_id:
        return None
    creds = google_integration.load_credentials_db()
    if not creds:
        return None
    service = build("sheets", "v4", credentials=creds)
    body = {"values": [values]}
    return service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range="A1",
        valueInputOption="RAW",
        body=body,
    ).execute()


def send_contact_email(name: str, email: str, message: str):
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USERNAME") or os.environ.get("GMAIL_USERNAME")
    smtp_password = os.environ.get("SMTP_PASSWORD") or os.environ.get("GMAIL_PASSWORD")
    to_email = os.environ.get("SMTP_TO") or os.environ.get("GMAIL_TO") or smtp_user
    if not smtp_user or not smtp_password:
        return {"status": "queued", "message": "Email delivery is not configured yet. The contact request is captured locally."}

    email_msg = EmailMessage()
    email_msg["Subject"] = f"New contact request from {name}"
    email_msg["From"] = smtp_user
    email_msg["To"] = to_email
    email_msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(email_msg)

    return {"status": "sent", "message": "Message sent successfully."}


@app.get("/", response_class=FileResponse, tags=["ui"])
def root():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


@app.get("/about", response_class=FileResponse, tags=["ui"])
def about_page():
    return FileResponse(os.path.join(BASE_DIR, "about.html"))


@app.get("/media", response_class=FileResponse, tags=["ui"])
def media_page():
    return FileResponse(os.path.join(BASE_DIR, "media.html"))


@app.get("/registration", response_class=FileResponse, tags=["ui"])
def registration_page():
    return FileResponse(os.path.join(BASE_DIR, "registration.html"))


@app.get("/contact", response_class=FileResponse, tags=["ui"])
def contact_page():
    return FileResponse(os.path.join(BASE_DIR, "contact.html"))


@app.get("/work", response_class=FileResponse, tags=["ui"])
def work_page():
    return FileResponse(os.path.join(BASE_DIR, "work.html"))


@app.get("/admin", response_class=FileResponse, tags=["ui"])
def admin_page():
    return FileResponse(os.path.join(BASE_DIR, "admin.html"))


@app.post("/sponsors/", response_model=schemas.Sponsor, tags=["sponsors"])
def create_sponsor(sponsor: schemas.SponsorCreate, db: Session = Depends(get_db)):
    existing_name = db.query(models.Sponsor).filter(models.Sponsor.name == sponsor.name).first()
    if existing_name:
        raise HTTPException(status_code=400, detail="Sponsor with this name already exists")
    existing_email = db.query(models.Sponsor).filter(models.Sponsor.email == sponsor.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Sponsor with this email already exists")
    sponsor_data = sponsor.dict(exclude={"password"})
    db_sponsor = models.Sponsor(**sponsor_data)
    db_sponsor.set_password(sponsor.password)
    db.add(db_sponsor)
    db.commit()
    db.refresh(db_sponsor)
    try:
        append_to_google_sheet([
            db_sponsor.name,
            db_sponsor.email,
            db_sponsor.phone or "",
            db_sponsor.status,
            db_sponsor.notes or "",
            "sponsor",
        ])
    except Exception as e:
        print(f"Error appending to Google Sheet: {e}")
    return db_sponsor


@app.get("/sponsors/", response_model=list[schemas.Sponsor], tags=["sponsors"])
def list_sponsors(skip: int = 0, limit: int = 100, search: str | None = None, status: str | None = None, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    query = db.query(models.Sponsor)
    if search:
        filter_value = f"%{search}%"
        query = query.filter(
            or_(
                models.Sponsor.name.ilike(filter_value),
                models.Sponsor.email.ilike(filter_value),
                models.Sponsor.phone.ilike(filter_value),
                models.Sponsor.status.ilike(filter_value),
                models.Sponsor.notes.ilike(filter_value),
            )
        )
    if status:
        query = query.filter(models.Sponsor.status == status)
    return query.offset(skip).limit(limit).all()


@app.get("/sponsors/{sponsor_id}", response_model=schemas.Sponsor, tags=["sponsors"])
def get_sponsor(sponsor_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    sponsor = db.query(models.Sponsor).filter(models.Sponsor.id == sponsor_id).first()
    if not sponsor:
        raise HTTPException(status_code=404, detail="Sponsor not found")
    return sponsor


@app.put("/sponsors/{sponsor_id}", response_model=schemas.Sponsor, tags=["sponsors"])
def update_sponsor(sponsor_id: int, sponsor_update: schemas.SponsorUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    sponsor = db.query(models.Sponsor).filter(models.Sponsor.id == sponsor_id).first()
    if not sponsor:
        raise HTTPException(status_code=404, detail="Sponsor not found")
    update_data = sponsor_update.dict(exclude_unset=True)
    if "email" in update_data:
        existing_email = db.query(models.Sponsor).filter(models.Sponsor.email == update_data["email"], models.Sponsor.id != sponsor_id).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Sponsor email already used by another sponsor")
    if "name" in update_data:
        existing_name = db.query(models.Sponsor).filter(models.Sponsor.name == update_data["name"], models.Sponsor.id != sponsor_id).first()
        if existing_name:
            raise HTTPException(status_code=400, detail="Sponsor name already used by another sponsor")
    if "password" in update_data:
        sponsor.set_password(update_data.pop("password"))
    for field, value in update_data.items():
        setattr(sponsor, field, value)
    db.commit()
    db.refresh(sponsor)
    return sponsor


@app.delete("/sponsors/{sponsor_id}", status_code=204, tags=["sponsors"])
def delete_sponsor(sponsor_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    sponsor = db.query(models.Sponsor).filter(models.Sponsor.id == sponsor_id).first()
    if not sponsor:
        raise HTTPException(status_code=404, detail="Sponsor not found")
    db.delete(sponsor)
    db.commit()
    return None


@app.post("/clients/", response_model=schemas.Client, tags=["clients"])
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    existing_name = db.query(models.Client).filter(models.Client.name == client.name).first()
    if existing_name:
        raise HTTPException(status_code=400, detail="Client with this name already exists")
    existing_email = db.query(models.Client).filter(models.Client.email == client.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Client with this email already exists")
    if client.sponsor_id:
        sponsor = db.query(models.Sponsor).filter(models.Sponsor.id == client.sponsor_id).first()
        if not sponsor:
            raise HTTPException(status_code=400, detail="Assigned sponsor does not exist")
    client_data = client.dict(exclude={"password"})
    db_client = models.Client(**client_data)
    db_client.set_password(client.password)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    try:
        append_to_google_sheet([
            db_client.name,
            db_client.email,
            db_client.phone or "",
            db_client.company or "",
            db_client.status,
            db_client.sponsor_id or "",
            "client",
        ])
    except Exception as e:
        print(f"Error appending to Google Sheet: {e}")
    return db_client


@app.get("/sponsors/{sponsor_id}/clients", response_model=list[schemas.Client], tags=["sponsors"])
def list_sponsor_clients(sponsor_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    sponsor = db.query(models.Sponsor).filter(models.Sponsor.id == sponsor_id).first()
    if not sponsor:
        raise HTTPException(status_code=404, detail="Sponsor not found")
    return db.query(models.Client).filter(models.Client.sponsor_id == sponsor_id).offset(skip).limit(limit).all()


@app.get("/clients/", response_model=list[schemas.Client], tags=["clients"])
def list_clients(skip: int = 0, limit: int = 100, search: str | None = None, status: str | None = None, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    query = db.query(models.Client)
    if search:
        filter_value = f"%{search}%"
        query = query.filter(
            or_(
                models.Client.name.ilike(filter_value),
                models.Client.email.ilike(filter_value),
                models.Client.company.ilike(filter_value),
                models.Client.phone.ilike(filter_value),
                models.Client.status.ilike(filter_value),
                models.Client.notes.ilike(filter_value),
            )
        )
    if status:
        query = query.filter(models.Client.status == status)
    return query.offset(skip).limit(limit).all()


@app.get("/clients/{client_id}", response_model=schemas.Client, tags=["clients"])
def get_client(client_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@app.get("/summary", response_model=schemas.Summary, tags=["dashboard"])
def get_summary(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    total_sponsors = db.query(models.Sponsor).count()
    total_clients = db.query(models.Client).count()
    active_clients = db.query(models.Client).filter(models.Client.status == "active").count()
    prospect_sponsors = db.query(models.Sponsor).filter(models.Sponsor.status == "prospect").count()
    return schemas.Summary(
        total_sponsors=total_sponsors,
        total_clients=total_clients,
        active_clients=active_clients,
        prospect_sponsors=prospect_sponsors,
    )


@app.post("/auth/sponsor-login", response_model=schemas.LoginResponse, tags=["auth"])
def sponsor_login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    sponsor = db.query(models.Sponsor).filter(models.Sponsor.email == payload.email).first()
    if not sponsor or not sponsor.verify_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid sponsor credentials")
    db.commit()
    token = create_access_token({"sub": sponsor.email, "role": "sponsor"})
    return schemas.LoginResponse(role="sponsor", name=sponsor.name, message="Sponsor login successful", token=token)


@app.post("/auth/client-login", response_model=schemas.LoginResponse, tags=["auth"])
def client_login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.email == payload.email).first()
    if not client or not client.verify_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid client credentials")
    db.commit()
    token = create_access_token({"sub": client.email, "role": "client"})
    return schemas.LoginResponse(role="client", name=client.name, message="Client login successful", token=token)


@app.post("/auth/admin-login", response_model=schemas.LoginResponse, tags=["auth"])
def admin_login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(
        or_(models.Admin.email == payload.email, models.Admin.username == payload.email)
    ).first()
    if not admin or not admin.verify_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    db.commit()
    token = create_access_token({"sub": admin.email, "role": "admin"})
    return schemas.LoginResponse(role="admin", name=admin.username, message="Admin login successful", token=token)


@app.put("/admins/me", response_model=schemas.Admin, tags=["admin"])
def update_admin(admin_update: schemas.AdminUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    admin = db.query(models.Admin).filter(models.Admin.email == current_user.get("sub")).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
        
    if admin_update.username:
        admin.username = admin_update.username
    if admin_update.email:
        # Check if email is already taken
        existing = db.query(models.Admin).filter(models.Admin.email == admin_update.email).first()
        if existing and existing.id != admin.id:
            raise HTTPException(status_code=400, detail="Email already registered")
        admin.email = admin_update.email
    if admin_update.password:
        admin.set_password(admin_update.password)
        
    db.commit()
    db.refresh(admin)
    return admin



@app.put("/clients/{client_id}", response_model=schemas.Client, tags=["clients"])
def update_client(client_id: int, client_update: schemas.ClientUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    update_data = client_update.dict(exclude_unset=True)
    if "email" in update_data:
        existing_email = db.query(models.Client).filter(models.Client.email == update_data["email"], models.Client.id != client_id).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Client email already used by another client")
    if "name" in update_data:
        existing_name = db.query(models.Client).filter(models.Client.name == update_data["name"], models.Client.id != client_id).first()
        if existing_name:
            raise HTTPException(status_code=400, detail="Client name already used by another client")
    if "sponsor_id" in update_data:
        sponsor_id = update_data["sponsor_id"]
        if sponsor_id:
            sponsor = db.query(models.Sponsor).filter(models.Sponsor.id == sponsor_id).first()
            if not sponsor:
                raise HTTPException(status_code=400, detail="Assigned sponsor does not exist")
    if "password" in update_data:
        client.set_password(update_data.pop("password"))
    for field, value in update_data.items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client


@app.delete("/clients/{client_id}", status_code=204, tags=["clients"])
def delete_client(client_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return None


@app.post("/contact/message", response_model=schemas.MessageResponse, tags=["contact"])
def submit_contact_message(payload: schemas.ContactMessageCreate, db: Session = Depends(get_db)):
    try:
        db_msg = models.ContactMessage(
            name=payload.name,
            email=payload.email,
            message=payload.message
        )
        db.add(db_msg)
        db.commit()
    except Exception as e:
        print(f"Error saving to DB: {e}")
        
    result = send_contact_email(payload.name, payload.email, payload.message)
    return {"status": result["status"], "message": result["message"]}

@app.post("/marketing/campaigns", response_model=schemas.MarketingCampaignCreate, tags=["marketing"])
def create_marketing_campaign(payload: schemas.MarketingCampaignCreate, db: Session = Depends(get_db)):
    try:
        db_camp = models.MarketingCampaign(
            title=payload.title,
            platform=payload.platform,
            status=payload.status,
            metrics=payload.metrics
        )
        db.add(db_camp)
        db.commit()
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/chat/assistant", response_model=schemas.ChatResponse, tags=["chat"])
def chat_assistant(payload: schemas.ChatRequest):
    message = payload.message.strip().lower()
    if not message:
        raise HTTPException(status_code=400, detail="Please enter a question")
    if any(keyword in message for keyword in ["about", "who", "company"]):
        reply = "R-Abhi Tech Solution helps brands, sponsors, and clients manage campaigns, registrations, and growth in one modern portal."
    elif any(keyword in message for keyword in ["media", "social", "marketing"]):
        reply = "We can plan social media campaigns, sponsor activations, influencer outreach, and performance reports from the media workspace."
    elif any(keyword in message for keyword in ["register", "signup", "join"]):
        reply = "You can register as a sponsor or client from the registration page and start managing your account right away."
    elif any(keyword in message for keyword in ["contact", "help", "support"]):
        reply = "You can reach our team through the contact page or use the admin dashboard for portal management."
    else:
        reply = "I can help with sponsorship planning, client onboarding, media campaigns, and portal navigation."
    return {"reply": reply}
