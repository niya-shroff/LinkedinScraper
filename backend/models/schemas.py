from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional

class ScrapeRequest(BaseModel):
    email: EmailStr
    password: str
    profile_url: HttpUrl

class ProfileData(BaseModel):
    name: Optional[str] = None
    position: Optional[str] = None
    company: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    total_time: Optional[str] = None
    summary: Optional[str] = None
    position: Optional[str] = None
    company: Optional[str] = None

class ScrapeResponse(BaseModel):
    success: bool
    data: Optional[ProfileData] = None
    message: Optional[str] = None