from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class SponsorBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    status: Optional[str] = "prospect"
    notes: Optional[str] = None


class SponsorCreate(SponsorBase):
    password: str


class SponsorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    password: Optional[str] = None


class Sponsor(SponsorBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    sponsor_id: Optional[int] = None
    status: Optional[str] = "active"
    notes: Optional[str] = None


class ClientCreate(ClientBase):
    password: str


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    sponsor_id: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    password: Optional[str] = None


class Client(ClientBase):
    id: int
    sponsor_id: Optional[int] = None
    sponsor_name: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class AdminBase(BaseModel):
    username: str
    email: EmailStr


class AdminCreate(AdminBase):
    password: str


class AdminUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class Admin(AdminBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    role: str
    name: str
    message: str
    token: str


class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    message: str


class ChatRequest(BaseModel):
    message: str


class MessageResponse(BaseModel):
    status: str
    message: str


class ChatResponse(BaseModel):
    reply: str


class Summary(BaseModel):
    total_sponsors: int
    total_clients: int
    active_clients: int
    prospect_sponsors: int

    class Config:
        orm_mode = True

class ContactMessageCreate(BaseModel):
    name: str
    email: EmailStr
    message: str

class MarketingCampaignCreate(BaseModel):
    title: str
    platform: str
    status: Optional[str] = "planning"
    metrics: Optional[str] = None


class EmailCampaignRequest(BaseModel):
    recipient_email: Optional[str] = None  # Specific email or target group like "all_sponsors", "all_clients"
    target_group: Optional[str] = "custom"  # "custom", "all_sponsors", "all_clients", "all_users"
    subject: str
    body: str
    template_name: Optional[str] = "default"  # "default", "sponsor_invite", "campaign_update", "promo"


class EmailCampaignResponse(BaseModel):
    status: str
    delivered_count: int
    failed_count: int
    message: str

