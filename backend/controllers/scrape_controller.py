from fastapi import APIRouter
from app.models.schemas import ScrapeRequest, ScrapeResponse
from app.services.linkedin_service import LinkedInService

router = APIRouter()

@router.post("/api/scrape", response_model=ScrapeResponse, summary="Scrape LinkedIn profile")
async def scrape_profile(request: ScrapeRequest):
    """
    Scrape a LinkedIn profile using provided LinkedIn credentials.

    Returns:
        ScrapeResponse containing profile data or error message
    """
    profile_data = LinkedInService.scrape_profile(
        email=request.email,
        password=request.password,
        profile_url=str(request.profile_url)
    )
    return ScrapeResponse(success=True, data=profile_data, message="Profile scraped successfully")