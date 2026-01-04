"""
LinkedIn Profile Scraper Module
Handles the scraping logic for LinkedIn profiles
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re
import os
from typing import Dict, Optional


class LinkedInScraper:
    """LinkedIn profile scraper class"""
    
    def __init__(self, chromedriver_path: Optional[str] = None):
        """
        Initialize the scraper
        
        Args:
            chromedriver_path: Path to chromedriver executable. 
                             If None, will try to use CHROMEDRIVER_PATH env var or default path
        """
        self.chromedriver_path = chromedriver_path or os.getenv(
            'CHROMEDRIVER_PATH', 
            '/usr/local/bin/chromedriver'  # Default path for Docker/Linux
        )
        self.driver = None
    
    def _setup_driver(self):
        """Setup Chrome driver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode for Docker
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        service = Service(self.chromedriver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        return self.driver
    
    def login(self, email: str, password: str) -> bool:
        """
        Login to LinkedIn
        
        Args:
            email: LinkedIn email
            password: LinkedIn password
            
        Returns:
            True if login successful, False otherwise
        """
        try:
            if not self.driver:
                self._setup_driver()
            
            self.driver.get("https://linkedin.com/uas/login")
            time.sleep(3)
            
            # Wait for and fill username
            username = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username.send_keys(email)
            
            # Fill password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(password)
            
            # Click submit
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            
            # Wait a bit for login to complete
            time.sleep(5)
            
            # Check if login was successful (not on login page anymore)
            if "feed" in self.driver.current_url or "linkedin.com/in/" in self.driver.current_url:
                return True
            return False
            
        except Exception as e:
            print(f"Login error: {str(e)}")
            return False
    
    def scrape_profile(self, profile_url: str) -> Dict[str, str]:
        """
        Scrape a LinkedIn profile
        
        Args:
            profile_url: URL of the LinkedIn profile to scrape
            
        Returns:
            Dictionary containing scraped profile data
        """
        if not self.driver:
            raise Exception("Driver not initialized. Please login first.")
        
        try:
            # Navigate to profile
            self.driver.get(profile_url)
            time.sleep(3)
            
            # Scroll to load all content
            self._scroll_page()
            
            # Parse the page
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            
            # Extract data
            data = self._extract_profile_data(soup)
            return data
            
        except Exception as e:
            raise Exception(f"Error scraping profile: {str(e)}")
    
    def _scroll_page(self, scroll_timeout: int = 20):
        """
        Scroll the page to load all content
        
        Args:
            scroll_timeout: Maximum time to spend scrolling (seconds)
        """
        start = time.time()
        initial_scroll = 0
        final_scroll = 1000
        
        while True:
            self.driver.execute_script(f"window.scrollTo({initial_scroll},{final_scroll})")
            initial_scroll = final_scroll
            final_scroll += 1000
            time.sleep(3)
            
            end = time.time()
            if round(end - start) > scroll_timeout:
                break
    
    def _extract_profile_data(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extract profile data from BeautifulSoup object
        
        Args:
            soup: BeautifulSoup object of the profile page
            
        Returns:
            Dictionary with extracted profile data
        """
        data = {
            "name": "",
            "position": "",
            "company": "",
            "start_time": "",
            "end_time": "",
            "total_time": "",
            "summary": ""
        }
        
        try:
            # Extract name
            intro = soup.find('div', {'class': 'pv-text-details__left-panel'})
            if intro:
                name_element = intro.find("h1")
                if name_element:
                    data["name"] = name_element.get_text().strip()
            
            # Extract experience
            experience_sections = soup.find_all('div', {'class': 'pvs-list__outer-container'})
            if len(experience_sections) > 1:
                # Most recent experience
                position_element = experience_sections[1].find_all("span")
                if position_element and len(position_element) > 0:
                    position_span = position_element[0].find_all("span")
                    if position_span and len(position_span) > 0:
                        data["position"] = position_span[0].get_text().strip()
                
                # Company
                company_block = experience_sections[1].find('div', {'class': 'display-flex flex-column full-width'})
                if company_block:
                    company_span = company_block.find("span", {'class': 't-14 t-normal'})
                    if company_span:
                        company_spans = company_span.find_all("span")
                        if company_spans:
                            data["company"] = company_spans[0].get_text().strip()
                    
                    # Time frame
                    time_block = company_block.find("span", {'class': 't-14 t-normal t-black--light'})
                    if time_block:
                        time_spans = time_block.find_all("span")
                        if time_spans:
                            time_text = time_spans[0].get_text().strip()
                            
                            # Parse time information
                            if "-" in time_text:
                                start_time = re.split("-", time_text)[0].strip()
                                start_time_end_index = time_text.find("-")
                                end_time_index = time_text.find("·")
                                
                                if end_time_index != -1:
                                    end_time = time_text[(start_time_end_index + 1):end_time_index].strip()
                                    total_time = time_text[(end_time_index + 1):].strip()
                                else:
                                    end_time = time_text[(start_time_end_index + 1):].strip()
                                    total_time = ""
                                
                                data["start_time"] = start_time
                                data["end_time"] = end_time
                                data["total_time"] = total_time
            
            # Create summary
            if data["name"] and data["position"] and data["company"]:
                summary = f"This person's name is {data['name']} and they work as a {data['position']} at {data['company']}."
                if data["start_time"] and data["end_time"]:
                    summary += f" They have worked there from {data['start_time']} to {data['end_time']}."
                if data["total_time"]:
                    summary += f" for a total of {data['total_time']}."
                data["summary"] = summary
            
        except Exception as e:
            print(f"Error extracting data: {str(e)}")
        
        return data
    
    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

