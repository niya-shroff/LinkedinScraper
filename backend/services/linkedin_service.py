import os
from fastapi import HTTPException
from models.schemas import ProfileData
from scraper.linkedin_scraper import LinkedInScraper

class LinkedInService:
    """Service layer for LinkedIn scraping"""

    @staticmethod
    def scrape_profile(email: str, password: str, profile_url: str) -> ProfileData:
        chromedriver_path = os.getenv("CHROMEDRIVER_PATH")

        try:
            # Context manager ensures proper cleanup
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
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while scraping: {str(e)}"
            )