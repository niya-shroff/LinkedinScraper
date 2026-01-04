"""
LinkedIn Service Layer
Handles business logic for LinkedIn scraping
"""

import os
from fastapi import HTTPException
from app.models.schemas import ProfileData
from app.scraper.linkedin_scraper import LinkedInScraper


class LinkedInService:
    """Service for scraping LinkedIn profiles"""

    @staticmethod
    def scrape_profile(email: str, password: str, profile_url: str) -> ProfileData:
        """
        Scrape a LinkedIn profile using LinkedInScraper

        Args:
            email: LinkedIn email
            password: LinkedIn password
            profile_url: LinkedIn profile URL

        Returns:
            ProfileData: Pydantic model with profile info
        """
        chromedriver_path = os.getenv("CHROMEDRIVER_PATH")

        try:
            # Use context manager to ensure driver is closed
            with LinkedInScraper(chromedriver_path=chromedriver_path) as scraper:
                # Login
                if not scraper.login(email, password):
                    raise HTTPException(
                        status_code=401,
                        detail="Failed to login. Check your LinkedIn credentials."
                    )

                # Scrape profile
                profile_data = scraper.scrape_profile(profile_url)

                if not profile_data.get("name"):
                    raise HTTPException(
                        status_code=404,
                        detail="Could not extract profile data. Profile may be private or URL invalid."
                    )

                return ProfileData(**profile_data)

        except HTTPException:
            # Reraise known FastAPI HTTPExceptions
            raise
        except Exception as e:
            # Catch all other exceptions
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while scraping: {str(e)}"
            )