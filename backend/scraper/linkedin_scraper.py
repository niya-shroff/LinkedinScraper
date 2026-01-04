"""
LinkedIn Profile Scraper Module
Handles scraping logic for LinkedIn profiles using Selenium and BeautifulSoup
"""

import os
import time
import re
from typing import Dict, Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class LinkedInScraper:
    """LinkedIn profile scraper"""

    def __init__(self, chromedriver_path: Optional[str] = None):
        """
        Initialize the scraper

        Args:
            chromedriver_path: Path to chromedriver executable.
                              If None, will use CHROMEDRIVER_PATH env var or default path
        """
        self.chromedriver_path = chromedriver_path or os.getenv(
            'CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver'
        )
        self.driver: Optional[webdriver.Chrome] = None

    def _setup_driver(self) -> webdriver.Chrome:
        """Setup Chrome driver with options"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )

        service = Service(self.chromedriver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        return self.driver

    def login(self, email: str, password: str) -> bool:
        """
        Login to LinkedIn

        Returns:
            True if login successful, False otherwise
        """
        if not self.driver:
            self._setup_driver()

        try:
            self.driver.get("https://linkedin.com/uas/login")
            time.sleep(2)

            # Enter credentials
            username = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username.send_keys(email)

            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(password)

            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()

            time.sleep(3)

            # Check login success
            if "feed" in self.driver.current_url or "linkedin.com/in/" in self.driver.current_url:
                return True

            return False
        except Exception as e:
            print(f"[LinkedInScraper] Login error: {str(e)}")
            return False

    def scrape_profile(self, profile_url: str) -> Dict[str, str]:
        """
        Scrape LinkedIn profile data

        Args:
            profile_url: LinkedIn profile URL

        Returns:
            Dictionary of profile info
        """
        if not self.driver:
            raise Exception("Driver not initialized. Call login first.")

        try:
            self.driver.get(profile_url)
            time.sleep(2)
            self._scroll_page()

            soup = BeautifulSoup(self.driver.page_source, "lxml")
            data = self._extract_profile_data(soup)
            return data
        except Exception as e:
            raise Exception(f"Error scraping profile: {str(e)}")

    def _scroll_page(self, scroll_timeout: int = 20):
        """Scroll the page to load dynamic content"""
        start_time = time.time()
        initial, final = 0, 1000

        while True:
            self.driver.execute_script(f"window.scrollTo({initial}, {final})")
            initial, final = final, final + 1000
            time.sleep(2)
            if time.time() - start_time > scroll_timeout:
                break

    def _extract_profile_data(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract profile information from BeautifulSoup object"""
        data = {
            "name": "",
            "position": "",
            "company": "",
            "start_time": "",
            "end_time": "",
            "total_time": "",
            "summary": "",
        }

        try:
            # Name
            intro = soup.find("div", {"class": "pv-text-details__left-panel"})
            if intro and intro.find("h1"):
                data["name"] = intro.find("h1").get_text().strip()

            # Experience
            experiences = soup.find_all("div", {"class": "pvs-list__outer-container"})
            if len(experiences) > 1:
                position_spans = experiences[1].find_all("span")
                if position_spans:
                    data["position"] = position_spans[0].get_text().strip()

                company_block = experiences[1].find("div", {"class": "display-flex flex-column full-width"})
                if company_block:
                    company_span = company_block.find("span", {"class": "t-14 t-normal"})
                    if company_span:
                        data["company"] = company_span.get_text().strip()

                    # Time frame
                    time_block = company_block.find("span", {"class": "t-14 t-normal t-black--light"})
                    if time_block:
                        time_text = time_block.get_text().strip()
                        if "-" in time_text:
                            parts = re.split("-", time_text)
                            data["start_time"] = parts[0].strip()
                            if len(parts) > 1:
                                remainder = parts[1].split("·")
                                data["end_time"] = remainder[0].strip()
                                if len(remainder) > 1:
                                    data["total_time"] = remainder[1].strip()

            # Summary
            if data["name"] and data["position"] and data["company"]:
                summary = f"{data['name']} works as {data['position']} at {data['company']}."
                if data["start_time"] and data["end_time"]:
                    summary += f" From {data['start_time']} to {data['end_time']}."
                if data["total_time"]:
                    summary += f" Total experience: {data['total_time']}."
                data["summary"] = summary

        except Exception as e:
            print(f"[LinkedInScraper] Data extraction error: {str(e)}")

        return data

    def close(self):
        """Close the Selenium driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    # Context manager support
    def __enter__(self):
        if not self.driver:
            self._setup_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()