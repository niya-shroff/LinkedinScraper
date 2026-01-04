"""
FastAPI Backend for LinkedIn Scraper
Provides REST API endpoints for scraping LinkedIn profiles
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Optional
import os
from dotenv import load_dotenv

from backend.scraper import LinkedInScraper

# Load environment variables
load_dotenv()

app = FastAPI(
    title="LinkedIn Scraper API",
    description="REST API for scraping LinkedIn profiles",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class ScrapeRequest(BaseModel):
    """Request model for scraping a profile"""
    email: EmailStr
    password: str
    profile_url: HttpUrl


class ProfileData(BaseModel):
    """Response model for profile data"""
    name: str
    position: str
    company: str
    start_time: str
    end_time: str
    total_time: str
    summary: str


class ScrapeResponse(BaseModel):
    """Response model for scrape endpoint"""
    success: bool
    data: Optional[ProfileData] = None
    message: Optional[str] = None


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "LinkedIn Scraper API", "status": "running"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/scrape", response_model=ScrapeResponse)
async def scrape_profile(request: ScrapeRequest):
    """
    Scrape a LinkedIn profile
    
    Args:
        request: ScrapeRequest containing email, password, and profile_url
        
    Returns:
        ScrapeResponse with profile data or error message
    """
    scraper = None
    try:
        # Get chromedriver path from environment or use default
        chromedriver_path = os.getenv('CHROMEDRIVER_PATH')
        
        # Initialize scraper
        scraper = LinkedInScraper(chromedriver_path=chromedriver_path)
        scraper._setup_driver()
        
        # Login
        login_success = scraper.login(request.email, request.password)
        if not login_success:
            raise HTTPException(
                status_code=401,
                detail="Failed to login to LinkedIn. Please check your credentials."
            )
        
        # Scrape profile
        profile_data = scraper.scrape_profile(str(request.profile_url))
        
        # Validate that we got meaningful data
        if not profile_data.get("name"):
            raise HTTPException(
                status_code=404,
                detail="Could not extract profile data. The profile may be private or the URL is invalid."
            )
        
        return ScrapeResponse(
            success=True,
            data=ProfileData(**profile_data),
            message="Profile scraped successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while scraping: {str(e)}"
        )
    finally:
        if scraper:
            scraper.close()


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    uvicorn.run(
        "backend.main:app",
        host=host,
        port=port,
        reload=debug
    )

