import os
from fastapi import HTTPException
from backend.scraper.linkedin_scraper import LinkedInScraper
from app.models.schemas import ProfileData

class LinkedInService:
    """Handles LinkedIn scraping business logic"""

    @staticmethod
    def scrape_profile(email: str, password: str, profile_url: str) -> ProfileData:
        scraper = None
        try:
            chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
            scraper = LinkedInScraper(chromedriver_path=chromedriver_path)
            scraper._setup_driver()

            if not scraper.login(email, password):
                raise HTTPException(status_code=401, detail="Invalid LinkedIn credentials.")

            profile_data = scraper.scrape_profile(profile_url)

            if not profile_data.get("name"):
                raise HTTPException(status_code=404, detail="Profile data not found.")

            return ProfileData(**profile_data)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Scraping error: {str(e)}")
        finally:
            if scraper:
                scraper.close()