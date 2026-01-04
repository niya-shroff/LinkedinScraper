import { useState } from 'react';
import './ScraperForm.css';

const ScraperForm = ({ onScrape, isLoading, backendStatus }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    profileUrl: '',
  });

  const [errors, setErrors] = useState({});

  const validateUrl = (url) => {
    try {
      const urlObj = new URL(url);
      return urlObj.hostname.includes('linkedin.com');
    } catch {
      return false;
    }
  };

  const validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const newErrors = {};

    // Validate email
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    // Validate password
    if (!formData.password.trim()) {
      newErrors.password = 'Password is required';
    }

    // Validate profile URL
    if (!formData.profileUrl.trim()) {
      newErrors.profileUrl = 'Profile URL is required';
    } else if (!validateUrl(formData.profileUrl)) {
      newErrors.profileUrl = 'Please enter a valid LinkedIn profile URL';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    onScrape(formData);
  };

  const isDisabled = isLoading || backendStatus !== 'connected';

  return (
    <form onSubmit={handleSubmit} className="scraper-form">
      <div className="form-group">
        <label htmlFor="email">Email Address</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="your.email@example.com"
          className={errors.email ? 'error' : ''}
          disabled={isDisabled}
        />
        {errors.email && <span className="error-message">{errors.email}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="password">Password</label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          placeholder="Enter your LinkedIn password"
          className={errors.password ? 'error' : ''}
          disabled={isDisabled}
        />
        {errors.password && <span className="error-message">{errors.password}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="profileUrl">LinkedIn Profile URL</label>
        <input
          type="url"
          id="profileUrl"
          name="profileUrl"
          value={formData.profileUrl}
          onChange={handleChange}
          placeholder="https://www.linkedin.com/in/profile-name/"
          className={errors.profileUrl ? 'error' : ''}
          disabled={isDisabled}
        />
        {errors.profileUrl && <span className="error-message">{errors.profileUrl}</span>}
      </div>

      <button 
        type="submit" 
        className="btn btn-primary"
        disabled={isDisabled}
      >
        {isLoading ? 'Scraping...' : 'Gather Data'}
      </button>

      {backendStatus !== 'connected' && (
        <div className="backend-warning">
          <p>⚠️ Backend server is not connected. Please make sure the backend is running on port 8000.</p>
        </div>
      )}
    </form>
  );
};

export default ScraperForm;

