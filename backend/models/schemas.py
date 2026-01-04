from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Optional

class ScrapeRequest(BaseModel):
    email: EmailStr
    password: str
    profile_url: HttpUrl

class ProfileData(BaseModel):
    name: str
    position: str
    company: str
    start_time: str
    end_time: str
    total_time: str
    summary: str

class ScrapeResponse(BaseModel):
    success: bool
    data: Optional[ProfileData] = None
    message: Optional[str] = None