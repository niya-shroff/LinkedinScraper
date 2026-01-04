from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import scrape_controller
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="LinkedIn Scraper API",
    description="REST API for scraping LinkedIn profiles",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(scrape_controller.router)

# Health check
@app.get("/")
async def root():
    return {"message": "LinkedIn Scraper API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"

    uvicorn.run("app.main:app", host=host, port=port, reload=debug)