# LinkedIn Scraper Frontend

Modern React frontend for the LinkedIn Scraper application.

## Features

- 🎨 Beautiful, modern UI with gradient design
- ⚡ Fast development with Vite
- 📱 Responsive design
- ✅ Form validation
- 🔄 Real-time backend status checking
- 🎯 Error handling and user feedback

## Development

### Prerequisites

- Node.js 18+ and npm

### Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`

3. **Build for production:**
   ```bash
   npm run build
   ```

4. **Preview production build:**
   ```bash
   npm run preview
   ```

## Environment Variables

Create a `.env` file in the frontend directory (optional):

```env
VITE_API_URL=http://localhost:8000
```

If not set, it defaults to `http://localhost:8000`.

## Docker

The frontend is containerized and can be run with Docker Compose from the root directory:

```bash
docker-compose up frontend
```

Or build the frontend Docker image separately:

```bash
docker build -t linkedin-scraper-frontend ./frontend
docker run -p 3000:80 linkedin-scraper-frontend
```

## Project Structure

```
frontend/
├── src/
│   ├── components/      # React components
│   │   ├── ScraperForm.jsx
│   │   └── ProfileResults.jsx
│   ├── services/        # API services
│   │   └── api.js
│   ├── App.jsx          # Main app component
│   ├── App.css
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── public/              # Static assets
├── Dockerfile           # Docker configuration
├── nginx.conf           # Nginx configuration
└── package.json
└── vite.config.js       # Vite configuration
```

## API Integration

The frontend communicates with the backend API at `/api/scrape`. The API service is configured in `src/services/api.js`.

### Example Usage

```javascript
import { scrapeProfile } from './services/api';

const result = await scrapeProfile(
  'email@example.com',
  'password',
  'https://www.linkedin.com/in/profile/'
);
```

## Technologies

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **CSS3** - Styling with modern features

