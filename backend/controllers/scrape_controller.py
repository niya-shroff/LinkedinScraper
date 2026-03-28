from fastapi import APIRouter
from backend.models.schemas import ScrapeRequest, ScrapeResponse
from backend.services.linkedin_service import LinkedInService

router = APIRouter()

@router.post("/api/scrape", response_model=ScrapeResponse, summary="Scrape LinkedIn profile")
async def scrape_profile(request: ScrapeRequest):
    """
    Scrape a LinkedIn profile using provided LinkedIn credentials.

    Returns:
        ScrapeResponse containing profile data or error message
    """
    profile_data = await LinkedInService.scrape_profile(
        email=request.email,
        password=request.password,
        profile_url=str(request.profile_url)
    )
    return ScrapeResponse(success=True, data=profile_data, message="Profile scraped successfully")