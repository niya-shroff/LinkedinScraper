from fastapi import HTTPException
from backend.models.schemas import ProfileData
from backend.scraper.linkedin_scraper import LinkedInScraper


class LinkedInService:
    """Service layer for LinkedIn scraping"""

    @staticmethod
    async def scrape_profile(
        email: str,
        password: str,
        profile_url: str
    ) -> ProfileData:
        scraper = LinkedInScraper()

        try:
            # Setup browser
            await scraper._setup()

            # Login
            success = await scraper.login(email, password)
            if not success:
                raise HTTPException(
                    status_code=401,
                    detail="Failed to login. Check your LinkedIn credentials."
                )

            # Scrape
            profile_data = await scraper.scrape_profile(profile_url)

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

        finally:
            await scraper.close()