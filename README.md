# LinkedIn Scraper

A modern LinkedIn profile scraper with a REST API backend and React frontend.

## Features

- Secure LinkedIn authentication
- Profile data extraction (name, position, company, work duration)
- FastAPI REST API backend
- Modern React frontend with beautiful UI
- Docker containerization support
- Responsive design

## Project Structure

```
LinkedinScraper/
├── backend/              # Backend API code
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   └── scraper.py       # LinkedIn scraping logic
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API services
│   │   └── App.jsx      # Main app
│   ├── Dockerfile       # Frontend Docker config
│   └── package.json
├── Dockerfile           # Backend Docker configuration
├── docker-compose.yml   # Docker Compose configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Prerequisites

- Python 3.11 or higher
- Node.js 18+ and npm (for frontend)
- pip (Python package manager)
- Docker and Docker Compose (optional, for containerized deployment)
- ChromeDriver (for local development without Docker)

## Setup

### Option 1: Local Development

#### Backend Setup

1. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```env
   CHROMEDRIVER_PATH=/path/to/chromedriver
   HOST=0.0.0.0
   PORT=8000
   DEBUG=True
   ```

4. **Run the backend:**
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000` and will proxy API requests to the backend.

### Option 2: Docker Deployment (Recommended)

1. **Build and run both services with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

   This will start:
   - Backend API at `http://localhost:8000`
   - Frontend at `http://localhost:3000`

2. **Or run services individually:**
   ```bash
   # Backend only
   docker-compose up backend
   
   # Frontend only
   docker-compose up frontend
   ```

3. **Or build and run with Docker directly:**
   ```bash
   # Backend
   docker build -t linkedin-scraper-backend .
   docker run -p 8000:8000 linkedin-scraper-backend
   
   # Frontend
   cd frontend
   docker build -t linkedin-scraper-frontend .
   docker run -p 3000:80 linkedin-scraper-frontend
   ```

## API Documentation

Once the server is running, you can access:
- **Interactive API docs:** http://localhost:8000/docs
- **Alternative docs:** http://localhost:8000/redoc
- **Health check:** http://localhost:8000/health

## API Endpoints

### POST `/api/scrape`

Scrape a LinkedIn profile.

**Request Body:**
```json
{
  "email": "your_email@example.com",
  "password": "your_password",
  "profile_url": "https://www.linkedin.com/in/profile-name/"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "name": "John Doe",
    "position": "Software Engineer",
    "company": "Tech Company",
    "start_time": "Jan 2020",
    "end_time": "Present",
    "total_time": "3 yrs 11 mos",
    "summary": "This person's name is John Doe and they work as a Software Engineer at Tech Company. They have worked there from Jan 2020 to Present."
  },
  "message": "Profile scraped successfully"
}
```

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Frontend

The React frontend is located in the `frontend/` directory and provides a modern, user-friendly interface for the scraper.

### Features

- Beautiful gradient UI design
- Real-time backend status indicator
- Form validation
- Error handling and user feedback
- Responsive design for mobile and desktop
- Loading states and animations

### Development

See `frontend/README.md` for detailed frontend documentation.

### API Integration

The frontend uses the API service in `frontend/src/services/api.js` to communicate with the backend. The API is configured with CORS to work with React frontends running on:
- `http://localhost:3000` (Vite default)
- `http://localhost:5173` (Alternative Vite port)

To add more origins, update the `allow_origins` list in `backend/main.py`.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CHROMEDRIVER_PATH` | Path to ChromeDriver executable | `/usr/local/bin/chromedriver` (Docker) |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Enable debug mode | `False` |

## Development

### Running Tests

```bash
# Install test dependencies (if you add them)
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Style

The project uses standard Python conventions. Consider using:
- `black` for code formatting
- `flake8` or `pylint` for linting
- `mypy` for type checking

## Troubleshooting

### ChromeDriver Issues

If you encounter ChromeDriver errors:
1. **Docker:** ChromeDriver is automatically installed in the Docker image
2. **Local:** Download ChromeDriver matching your Chrome version from [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)

### Login Failures

- Ensure your LinkedIn credentials are correct
- LinkedIn may require additional verification (2FA, captcha)
- Check if your account is locked or restricted

### Profile Not Found

- Verify the profile URL is correct and accessible
- Some profiles may be private or restricted
- LinkedIn's HTML structure may have changed (update selectors in `scraper.py`)

## License

This project is for educational purposes. Please respect LinkedIn's Terms of Service and use responsibly.
