from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional

class ScrapeRequest(BaseModel):
    email: EmailStr
    password: str
    profile_url: HttpUrl

class ProfileData(BaseModel):
    name: str
    position: str
    company: str
    start_time: Optional[str] = ""
    end_time: Optional[str] = ""
    total_time: Optional[str] = ""
    summary: Optional[str] = ""

class ScrapeResponse(BaseModel):
    success: bool
    data: Optional[ProfileData] = None
    message: Optional[str] = None