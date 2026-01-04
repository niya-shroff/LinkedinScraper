import { useState, useEffect } from 'react';
import ScraperForm from './components/ScraperForm';
import ProfileResults from './components/ProfileResults';
import { checkHealth } from './services/api';
import './App.css';

function App() {
  const [profileData, setProfileData] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState('checking');

  useEffect(() => {
    // Check backend health on mount
    checkHealth()
      .then(() => setBackendStatus('connected'))
      .catch(() => setBackendStatus('disconnected'));
  }, []);

  const handleScrape = async (formData) => {
    setIsLoading(true);
    setError(null);
    setProfileData(null);

    try {
      const { scrapeProfile } = await import('./services/api');
      const result = await scrapeProfile(
        formData.email,
        formData.password,
        formData.profileUrl
      );

      if (result.success && result.data) {
        setProfileData(result.data);
      } else {
        setError(result.message || 'Failed to scrape profile');
      }
    } catch (err) {
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setProfileData(null);
    setError(null);
  };

  return (
    <div className="app-container">
      <div className="app-card">
        <header className="app-header">
          <h1>LinkedIn Profile Scraper</h1>
          <div className={`status-indicator ${backendStatus}`}>
            <span className="status-dot"></span>
            <span className="status-text">
              {backendStatus === 'connected' ? 'Backend Connected' : 
               backendStatus === 'checking' ? 'Checking...' : 
               'Backend Disconnected'}
            </span>
          </div>
        </header>

        {!profileData && !error && (
          <ScraperForm 
            onScrape={handleScrape} 
            isLoading={isLoading}
            backendStatus={backendStatus}
          />
        )}

        {isLoading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Scraping profile data... This may take a moment.</p>
          </div>
        )}

        {error && (
          <div className="error-container">
            <div className="error-icon">⚠️</div>
            <h3>Error</h3>
            <p>{error}</p>
            <button onClick={handleReset} className="btn btn-secondary">
              Try Again
            </button>
          </div>
        )}

        {profileData && (
          <ProfileResults 
            data={profileData} 
            onReset={handleReset}
          />
        )}
      </div>
    </div>
  );
}

export default App;

