import axios from 'axios';

// Use environment variable if set, otherwise use relative URLs for production
// or localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.PROD ? '' : 'http://localhost:8000');

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Scrape a LinkedIn profile
 * @param {string} email - LinkedIn email
 * @param {string} password - LinkedIn password
 * @param {string} profileUrl - LinkedIn profile URL
 * @returns {Promise} API response
 */
export const scrapeProfile = async (email, password, profileUrl) => {
  try {
    const response = await api.post('/api/scrape', {
      email,
      password,
      profile_url: profileUrl,
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      // Server responded with error status
      throw new Error(error.response.data.detail || 'An error occurred while scraping');
    } else if (error.request) {
      // Request made but no response
      throw new Error('Unable to connect to the server. Please make sure the backend is running.');
    } else {
      // Something else happened
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
};

/**
 * Check if the API is healthy
 * @returns {Promise} API response
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw new Error('Backend server is not available');
  }
};

export default api;

