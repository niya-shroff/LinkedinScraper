import asyncio
import logging
from typing import Dict, Optional

import zendriver as zd
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)


class LinkedInScraper:
    def __init__(self):
        self.browser: Optional[zd.Browser] = None
        self.tab: Optional[zd.Tab] = None

    # --------------------------
    # SETUP
    # --------------------------
    async def _setup(self):
        logging.info("Starting browser...")

        self.browser = await zd.start(
            headless=True,
            user_data_dir="/app/chrome-profile",
            browser_args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ],
        )

        logging.info("Browser started")

    # --------------------------
    # LOGIN
    # --------------------------
    async def login(self, email: str, password: str) -> bool:
        if not self.browser:
            await self._setup()

        logging.info("Opening LinkedIn...")
        self.tab = await self.browser.get("https://www.linkedin.com/")

        await self.tab.wait(3)

        # ✅ CASE 1: Already logged in
        try:
            await self.tab.find("Me", best_match=True)
            logging.info("Already logged in ✅")
            return True
        except:
            pass

        # ✅ CASE 2: Need login
        logging.info("Navigating to login page...")
        self.tab = await self.browser.get("https://www.linkedin.com/login")

        await self.tab.wait(3)

        try:
            username = await self.tab.select("#username")
            password_el = await self.tab.select("#password")

            logging.info("Entering credentials...")
            await username.send_keys(email)
            await password_el.send_keys(password)

            login_btn = await self.tab.select("button[type=submit]")
            await login_btn.click()

            logging.info("Waiting for login...")
            await self.tab.wait(5)

            # verify login
            try:
                await self.tab.find("Me", best_match=True)
                logging.info("Login successful ✅")
                return True
            except:
                logging.error("Login failed ❌")
                return False

        except Exception as e:
            logging.error(f"[Login Error] {e}")
            return False

    # --------------------------
    # SCRAPE PROFILE
    # --------------------------
    async def scrape_profile(self, profile_url: str) -> Dict[str, str]:
        if not self.browser:
            raise Exception("Browser not initialized")

        logging.info(f"Opening profile: {profile_url}")
        self.tab = await self.browser.get(profile_url)

        await self.tab.wait(5)

        logging.info("Scrolling...")
        for _ in range(5):
            await self.tab.scroll_down(500)
            await self.tab.wait(1)

        html = await self.tab.get_content()
        soup = BeautifulSoup(html, "lxml")

        return self._extract_profile_data(soup)

    # --------------------------
    # PARSER (FIXED)
    # --------------------------
    def _extract_profile_data(self, soup: BeautifulSoup) -> Dict[str, str]:
        data = {
            "name": "",
            "position": "",
            "company": "",
            "summary": "",
        }

        try:
            # ✅ Name
            name_tag = soup.select_one("h1")
            if name_tag:
                data["name"] = name_tag.get_text(strip=True)

            # ✅ Headline
            headline_tag = soup.select_one(".text-body-medium")
            if headline_tag:
                data["position"] = headline_tag.get_text(strip=True)

            # ✅ About section
            about_tag = soup.select_one("#about ~ div span")
            if about_tag:
                data["summary"] = about_tag.get_text(strip=True)

        except Exception as e:
            logging.error(f"[Parsing Error] {e}")

        logging.info(f"Extracted: {data}")
        return data

    # --------------------------
    # CLEANUP
    # --------------------------
    async def close(self):
        if self.browser:
            logging.info("Closing browser...")
            await self.browser.stop()
            logging.info("Browser closed")