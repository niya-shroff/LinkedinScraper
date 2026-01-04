# Quick Start Guide

Get up and running with the LinkedIn Scraper in minutes!

## 🚀 Quick Start with Docker (Easiest)

1. **Clone/navigate to the project directory**

2. **Start everything with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Open your browser:**
   - Frontend: http://localhost:3000
   - Backend API Docs: http://localhost:8000/docs

That's it! The application is ready to use.

## 🛠️ Local Development Setup

### Backend

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend:**
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the frontend:**
   ```bash
   npm run dev
   ```

4. **Open http://localhost:3000 in your browser**

## 📝 Using the Application

1. Enter your LinkedIn email and password
2. Enter the LinkedIn profile URL you want to scrape
3. Click "Gather Data"
4. Wait for the scraping to complete
5. View the extracted profile information

## 🔧 Troubleshooting

### Backend won't start
- Make sure Python 3.11+ is installed
- Check that port 8000 is not already in use
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Frontend won't start
- Make sure Node.js 18+ is installed
- Check that port 3000 is not already in use
- Verify all dependencies are installed: `npm install`

### Docker issues
- Make sure Docker and Docker Compose are installed and running
- Try rebuilding: `docker-compose up --build --force-recreate`
- Check logs: `docker-compose logs`

### ChromeDriver errors
- In Docker: ChromeDriver is automatically installed
- Locally: Download ChromeDriver matching your Chrome version
- Set `CHROMEDRIVER_PATH` in `.env` file

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out the [API documentation](http://localhost:8000/docs) when the backend is running
- Explore the code in `backend/` and `frontend/` directories

## 🆘 Need Help?

- Check the main [README.md](README.md) for more information
- Review error messages in the browser console (F12) or terminal
- Ensure both backend and frontend are running if developing locally

