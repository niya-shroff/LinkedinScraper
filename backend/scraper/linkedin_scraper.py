import asyncio
import logging
from typing import Dict, List, Optional

import zendriver as zd
from bs4 import BeautifulSoup, Tag

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

        # CASE 1: Already logged in
        try:
            if "feed" in self.tab.url or "linkedin.com/in/" in self.tab.url:
                logging.info("Already logged in via redirect")
                return True
        except Exception:
            pass

        # CASE 2: Need login
        logging.info("Navigating to login page...")
        self.tab = await self.browser.get("https://www.linkedin.com/login")
        await self.tab.wait(3)

        try:
            username = await self.tab.select("#username", timeout=10)
        except:
            logging.warning("Login form not found, trying direct navigation to feed...")
            await self.tab.get("https://www.linkedin.com/feed/")
            await self.tab.wait(3)
            if "feed" in self.tab.url:
                logging.info("Session still valid")
                return True
            logging.error("Session invalid")
            return False

        try:
            username = await self.tab.select("#username", timeout=10)
            password_el = await self.tab.select("#password", timeout=10)
            logging.info("Entering credentials...")
            await username.send_keys(email)
            await password_el.send_keys(password)

            login_btn = await self.tab.select("button[type=submit]")
            await login_btn.click()

            logging.info("Waiting for login...")
            await self.tab.wait(30)

            try:
                if "feed" in self.tab.url or "linkedin.com/in/" in self.tab.url:
                    logging.info("Login successful")
                    return True
            except Exception:
                logging.error("Login failed")
                return False

        except Exception as e:
            logging.error(f"[Login Error] {e}")
            return False

    # --------------------------
    # SCRAPE PROFILE
    # --------------------------
    async def scrape_profile(self, profile_url: str) -> Dict:
        if not self.browser:
            raise Exception("Browser not initialized")

        logging.info(f"Opening profile: {profile_url}")
        self.tab = await self.browser.get(profile_url)
        await self.tab.wait(30)

        logging.info("Scrolling to load all sections...")
        for _ in range(8):
            await self.tab.scroll_down(500)
            await self.tab.wait(30)

        html = await self.tab.get_content()
        if any(x in html.lower() for x in [
            "sign in to view",
            "security verification",
            "challenge",
            "captcha"
        ]):
            logging.error("Blocked or not logged in ❌")
            raise Exception("LinkedIn blocked the session or login failed")
        soup = BeautifulSoup(html, "lxml")

        return self._extract_profile_data(soup)

    # --------------------------
    # HELPERS
    # --------------------------
    def _get_section_by_heading(self, soup: BeautifulSoup, heading_text: str) -> Optional[Tag]:
        """Find a <section> that contains an <h2> matching heading_text."""
        for h2 in soup.find_all("h2"):
            if heading_text.lower() in h2.get_text(strip=True).lower():
                # Walk up to the enclosing <section>
                section = h2.find_parent("section")
                if section:
                    return section
        return None

    def _clean_text(self, tag: Optional[Tag]) -> str:
        if not tag:
            return ""
        return tag.get_text(separator=" ", strip=True)

    # --------------------------
    # PARSER
    # --------------------------
    def _extract_profile_data(self, soup: BeautifulSoup) -> Dict:
        data = {
            "name": "",
            "pronouns": "",
            "headline": "",
            "location": "",
            "followers": "",
            "connections": "",
            "about": "",
            "experience": [],
            "education": [],
            "certifications": [],
            "skills": [],
            "projects": [],
            "volunteering": [],
            "courses": [],
            "honors": [],
            "languages": [],
        }

        try:
            self._extract_top_card(soup, data)
            self._extract_about(soup, data)
            self._extract_experience(soup, data)
            self._extract_education(soup, data)
            self._extract_certifications(soup, data)
            self._extract_skills(soup, data)
            self._extract_projects(soup, data)
            self._extract_volunteering(soup, data)
            self._extract_courses(soup, data)
            self._extract_honors(soup, data)
            self._extract_languages(soup, data)

            if not data["name"] or "sign in" in data["name"].lower():
                raise Exception("Invalid scrape: not a real profile page")

        except Exception as e:
            logging.error(f"[Parsing Error] {e}")

        logging.info(f"Extracted profile for: {data.get('name')}")
        return data

    # --------------------------
    # TOP CARD
    # --------------------------
    def _extract_top_card(self, soup: BeautifulSoup, data: dict):
        # Name: <h2> inside a div with aria-label matching the name
        # Fallback: first <h1> or <h2> that looks like a name
        name_div = soup.find("div", attrs={"aria-label": True})
        if name_div:
            h2 = name_div.find("h2")
            if h2:
                data["name"] = h2.get_text(strip=True)

        # Broader fallback for name
        if not data["name"]:
            for h2 in soup.find_all("h2"):
                text = h2.get_text(strip=True)
                # Names are typically short and don't contain pipe chars
                if text and len(text) < 60 and "|" not in text and "Analytics" not in text:
                    data["name"] = text
                    break

        # Pronouns: small <p> near the name containing "She/Her", "He/Him" etc.
        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            if text in ("She/Her", "He/Him", "They/Them", "She/They", "He/They"):
                data["pronouns"] = text
                break

        # Headline: <p> with the tagline text (after name, before location)
        # In the HTML it appears right after the name h2 block
        # Strategy: find <p> tags that look like a headline (longer, has pipe or keywords)
        if data["name"]:
            name_h2 = None
            for h2 in soup.find_all("h2"):
                if data["name"] in h2.get_text(strip=True):
                    name_h2 = h2
                    break
            if name_h2:
                # Look for the next <p> siblings after name
                for sibling in name_h2.find_all_next("p", limit=5):
                    text = sibling.get_text(strip=True)
                    if text and len(text) > 10 and text not in (data["name"], data["pronouns"]):
                        data["headline"] = text
                        break

        # Location: <p> containing "Area", "United States", city patterns
        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            if any(kw in text for kw in ("Area", "Metropolitan", "United States", "Remote")):
                if len(text) < 80:
                    data["location"] = text
                    break

        # Followers / Connections: anchor tags with these texts
        for a in soup.find_all("a"):
            text = a.get_text(strip=True)
            if "followers" in text and not data["followers"]:
                data["followers"] = text
            if "connections" in text and not data["connections"]:
                data["connections"] = text

    # --------------------------
    # ABOUT
    # --------------------------
    def _extract_about(self, soup: BeautifulSoup, data: dict):
        section = self._get_section_by_heading(soup, "About")
        if not section:
            return

        # About text lives in a span with data-testid="expandable-text-box"
        box = section.find(attrs={"data-testid": "expandable-text-box"})
        if box:
            data["about"] = box.get_text(separator="\n", strip=True)

    # --------------------------
    # EXPERIENCE
    # --------------------------
    def _extract_experience(self, soup: BeautifulSoup, data: dict):
        section = self._get_section_by_heading(soup, "Experience")
        if not section:
            return

        entries = []
        # Each experience item is anchored by a link that leads to the edit form
        # More reliably: find all <p> tags with a bold-style title (role title)
        # Structure per item:
        #   p.title (bold) -> p.company -> p.dates -> p.location -> p.description
        # We identify item boundaries by the company logo <figure> or <hr> separators

        # Find all item containers: divs containing both a title <p> and a dates <p>
        # Using the pattern: title is in a <p> with specific positioning after company logo
        for item_div in section.find_all("div", recursive=True):
            # Each experience item has an anchor to an edit form with position ID
            edit_link = item_div.find("a", href=lambda h: h and "/edit/forms/position/" in h)
            if not edit_link:
                continue

            entry = {
                "title": "",
                "company": "",
                "type": "",
                "dates": "",
                "duration": "",
                "location": "",
                "description": "",
                "skills": "",
            }

            # Title: first bold-ish <p> inside the edit link container
            paragraphs = edit_link.find_all("p")
            if len(paragraphs) >= 1:
                entry["title"] = paragraphs[0].get_text(strip=True)
            if len(paragraphs) >= 2:
                # "Company · Type" pattern
                company_text = paragraphs[1].get_text(strip=True)
                if "·" in company_text:
                    parts = company_text.split("·", 1)
                    entry["company"] = parts[0].strip()
                    entry["type"] = parts[1].strip()
                else:
                    entry["company"] = company_text

            # Dates and location come AFTER the edit_link, as siblings
            parent = edit_link.find_parent("div")
            if parent:
                all_p = parent.find_all("p")
                for p in all_p:
                    text = p.get_text(strip=True)
                    # Dates pattern: "Aug 2025 - Present · 8 mos"
                    if any(
                        m in text
                        for m in ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
                    ) and ("·" in text or "-" in text or "Present" in text):
                        if not entry["dates"]:
                            entry["dates"] = text
                    # Location pattern
                    elif any(
                        kw in text
                        for kw in ("Area", "United States", "Remote", "Hybrid", "On-site")
                    ) and not entry["location"]:
                        entry["location"] = text

            # Description: expandable text box in the broader item container
            item_container = item_div.find_parent("div")
            if item_container:
                desc_box = item_container.find(attrs={"data-testid": "expandable-text-box"})
                if desc_box:
                    entry["description"] = desc_box.get_text(separator="\n", strip=True)

            # Skills line: anchor with "/skill-associations-details/"
            skills_link = item_div.find("a", href=lambda h: h and "skill-associations-details" in h)
            if skills_link:
                entry["skills"] = skills_link.get_text(strip=True)

            if entry["title"]:
                entries.append(entry)

        # Deduplicate by (title, company)
        seen = set()
        unique = []
        for e in entries:
            key = (e["title"], e["company"])
            if key not in seen:
                seen.add(key)
                unique.append(e)

        data["experience"] = unique

    # --------------------------
    # EDUCATION
    # --------------------------
    def _extract_education(self, soup: BeautifulSoup, data: dict):
        section = self._get_section_by_heading(soup, "Education")
        if not section:
            return

        entries = []
        for item_div in section.find_all("div", recursive=True):
            edit_link = item_div.find(
                "a", href=lambda h: h and "/details/education/edit/forms/" in h
            )
            if not edit_link:
                continue

            entry = {
                "school": "",
                "degree": "",
                "grade": "",
                "activities": "",
                "skills": "",
            }

            paragraphs = edit_link.find_all("p")
            if len(paragraphs) >= 1:
                entry["school"] = paragraphs[0].get_text(strip=True)
            if len(paragraphs) >= 2:
                entry["degree"] = paragraphs[1].get_text(strip=True)

            # Grade and activities from expandable text boxes
            parent = item_div.find_parent("div")
            if parent:
                all_p = parent.find_all("p")
                for p in all_p:
                    text = p.get_text(strip=True)
                    if text.startswith("Grade:") and not entry["grade"]:
                        entry["grade"] = text.replace("Grade:", "").strip()

                desc_box = parent.find(attrs={"data-testid": "expandable-text-box"})
                if desc_box:
                    entry["activities"] = desc_box.get_text(separator="\n", strip=True)

            skills_link = item_div.find(
                "a", href=lambda h: h and "skill-associations-details" in h
            )
            if skills_link:
                entry["skills"] = skills_link.get_text(strip=True)

            if entry["school"]:
                entries.append(entry)

        seen = set()
        unique = []
        for e in entries:
            if e["school"] not in seen:
                seen.add(e["school"])
                unique.append(e)

        data["education"] = unique

    # --------------------------
    # CERTIFICATIONS
    # --------------------------
    def _extract_certifications(self, soup: BeautifulSoup, data: dict):
        section = self._get_section_by_heading(soup, "Licenses")
        if not section:
            return

        entries = []
        # Each cert item has a company logo link + a credential link
        # Find all divs that contain a "Show credential" link or cert name patterns
        for item_div in section.find_all("div", recursive=True):
            cred_link = item_div.find(
                "a", attrs={"aria-label": lambda v: v and "Show credential" in v}
            )
            if not cred_link:
                continue

            entry = {
                "name": "",
                "issuer": "",
                "issued": "",
                "expires": "",
                "credential_id": "",
            }

            all_p = item_div.find_all("p")
            for p in all_p:
                text = p.get_text(strip=True)
                if not entry["name"] and text and len(text) > 3:
                    entry["name"] = text
                elif text.startswith("Issued"):
                    entry["issued"] = text
                elif text.startswith("Credential ID"):
                    entry["credential_id"] = text.replace("Credential ID", "").strip()

            # Issuer: from the company logo link aria-label
            logo_link = item_div.find(
                "a", href=lambda h: h and "linkedin.com/company/" in h
            )
            if logo_link:
                figure = logo_link.find("figure")
                if figure:
                    img = figure.find("img")
                    if img and img.get("alt"):
                        entry["issuer"] = img["alt"].replace(" logo", "")

            if entry["name"]:
                entries.append(entry)

        seen = set()
        unique = []
        for e in entries:
            if e["name"] not in seen:
                seen.add(e["name"])
                unique.append(e)

        data["certifications"] = unique

    # --------------------------
    # SKILLS
    # --------------------------
    def _extract_skills(self, soup: BeautifulSoup, data: dict):
        section = self._get_section_by_heading(soup, "Skills")
        if not section:
            return

        skills = []
        # Each skill entry has a <p> with the skill name (bold) + endorsement details
        # Skills are in nested divs; the name <p> has a sibling showing where it's endorsed
        for item_div in section.find_all("div", recursive=True):
            # Skill name: bold <p> that is short (skill names are typically < 50 chars)
            name_p = item_div.find("p")
            if not name_p:
                continue
            text = name_p.get_text(strip=True)
            if (
                text
                and len(text) < 60
                and text not in ("Skills", "Show all")
                and not text.startswith("Software Engineer")
                and not text.startswith("Show")
            ):
                # Check it's in a skill-item-like container (has endorsement sibling)
                endorsement_p = item_div.find(
                    "p", string=lambda s: s and ("at " in s or "Engineer" in s)
                )
                if endorsement_p or item_div.find("figure"):
                    if text not in skills:
                        skills.append(text)

        data["skills"] = skills

    # --------------------------
    # PROJECTS
    # --------------------------
    def _extract_projects(self, soup: BeautifulSoup, data: dict):
        section = self._get_section_by_heading(soup, "Projects")
        if not section:
            return

        entries = []
        for item_div in section.find_all("div", recursive=True):
            show_link = item_div.find(
                "a", attrs={"aria-label": lambda v: v and "Show" in v and "project" in v}
            )
            name_p = item_div.find("p", class_=lambda c: c and "_24740a10" in (c or ""))

            # Fallback: find a <p> with a date range sibling
            date_p = item_div.find(
                "p", string=lambda s: s and "–" in (s or "") and ("Present" in s or any(
                    m in s for m in ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
                ))
            )

            if not (show_link or date_p):
                continue

            entry = {
                "name": "",
                "dates": "",
                "associated_with": "",
                "url": "",
                "description": "",
            }

            all_p = item_div.find_all("p")
            for p in all_p:
                text = p.get_text(strip=True)
                if not entry["name"] and text and len(text) < 80:
                    entry["name"] = text
                elif "–" in text or "Present" in text:
                    entry["dates"] = text
                elif text.startswith("Associated with"):
                    entry["associated_with"] = text.replace("Associated with", "").strip()

            if show_link:
                entry["url"] = show_link.get("href", "")

            desc_box = item_div.find(attrs={"data-testid": "expandable-text-box"})
            if desc_box:
                entry["description"] = desc_box.get_text(separator="\n", strip=True)

            if entry["name"]:
                entries.append(entry)

        seen = set()
        unique = []
        for e in entries:
            if e["name"] not in seen:
                seen.add(e["name"])
                unique.append(e)

        data["projects"] = unique

    # --------------------------
    # VOLUNTEERING
    # --------------------------
    def _extract_volunteering(self, soup: BeautifulSoup, data: dict):
        section = self._get_section_by_heading(soup, "Volunteering")
        if not section:
            return

        entries = []
        for item_div in section.find_all("div", recursive=True):
            edit_link = item_div.find(
                "a", href=lambda h: h and "/volunteer-experiences/edit/forms/" in h
            )
            if not edit_link:
                continue

            entry = {
                "role": "",
                "organization": "",
                "dates": "",
                "cause": "",
                "description": "",
            }

            paragraphs = edit_link.find_all("p")
            if len(paragraphs) >= 1:
                entry["role"] = paragraphs[0].get_text(strip=True)
            if len(paragraphs) >= 2:
                entry["organization"] = paragraphs[1].get_text(strip=True)

            parent = item_div.find_parent("div")
            if parent:
                for p in parent.find_all("p"):
                    text = p.get_text(strip=True)
                    if any(
                        m in text
                        for m in ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
                    ) and not entry["dates"]:
                        entry["dates"] = text
                    elif len(text) < 30 and not any(
                        c.isdigit() for c in text
                    ) and text not in (entry["role"], entry["organization"]) and not entry["cause"]:
                        entry["cause"] = text

                desc_box = parent.find(attrs={"data-testid": "expandable-text-box"})
                if desc_box:
                    entry["description"] = desc_box.get_text(separator="\n", strip=True)

            if entry["role"]:
                entries.append(entry)

        seen = set()
        unique = []
        for e in entries:
            key = (e["role"], e["organization"])
            if key not in seen:
                seen.add(key)
                unique.append(e)

        data["volunteering"] = unique

    # --------------------------
    # COURSES
    # --------------------------
    def _extract_courses(self, soup: BeautifulSoup, data: dict):
        section = self._get_section_by_heading(soup, "Courses")
        if not section:
            return

        courses = []
        # Each course has a name <p> + course code <p> + associated school
        for item_div in section.find_all("div", recursive=True):
            all_p = item_div.find_all("p", recursive=False)
            # Look for divs that have exactly 2 short <p>s (name + code)
            if len(all_p) < 2:
                # Try non-recursive
                all_p = item_div.find_all("p")

            name = ""
            code = ""
            associated = ""

            for p in all_p:
                text = p.get_text(strip=True)
                if text.startswith("Associated with"):
                    associated = text.replace("Associated with", "").strip()
                elif text and not name and len(text) < 80:
                    name = text
                elif text and not code and len(text) < 30:
                    code = text

            if name and name not in ("Courses", "Show all") and associated:
                entry = {
                    "name": name,
                    "code": code,
                    "associated_with": associated,
                }
                if entry not in courses:
                    courses.append(entry)

        data["courses"] = courses

    # --------------------------
    # HONORS & AWARDS
    # --------------------------
    def _extract_honors(self, soup: BeautifulSoup, data: dict):
        section = self._get_section_by_heading(soup, "Honors")
        if not section:
            return

        entries = []
        for item_div in section.find_all("div", recursive=True):
            all_p = item_div.find_all("p")
            name = ""
            issuer = ""
            description = ""
            associated = ""

            for p in all_p:
                text = p.get_text(strip=True)
                if text.startswith("Issued by"):
                    issuer = text.replace("Issued by", "").strip()
                elif text.startswith("Associated with"):
                    associated = text.replace("Associated with", "").strip()

            desc_box = item_div.find(attrs={"data-testid": "expandable-text-box"})
            if desc_box:
                description = desc_box.get_text(separator="\n", strip=True)

            # Name: first bold short <p> that's not issuer/associated
            for p in all_p:
                text = p.get_text(strip=True)
                if (
                    text
                    and len(text) < 100
                    and not text.startswith("Issued")
                    and not text.startswith("Associated")
                    and text not in ("Honors & awards", "Show all")
                ):
                    name = text
                    break

            if name and issuer:
                entries.append({
                    "name": name,
                    "issuer": issuer,
                    "associated_with": associated,
                    "description": description,
                })

        seen = set()
        unique = []
        for e in entries:
            if e["name"] not in seen:
                seen.add(e["name"])
                unique.append(e)

        data["honors"] = unique

    # --------------------------
    # LANGUAGES
    # --------------------------
    def _extract_languages(self, soup: BeautifulSoup, data: dict):
        section = self._get_section_by_heading(soup, "Languages")
        if not section:
            return

        languages = []
        for item_div in section.find_all("div", recursive=True):
            all_p = item_div.find_all("p")
            name = ""
            proficiency = ""

            for p in all_p:
                text = p.get_text(strip=True)
                if "proficiency" in text.lower() and not proficiency:
                    proficiency = text
                elif (
                    text
                    and not name
                    and len(text) < 40
                    and "proficiency" not in text.lower()
                    and text not in ("Languages", "Show all")
                ):
                    name = text

            if name and proficiency:
                entry = {"language": name, "proficiency": proficiency}
                if entry not in languages:
                    languages.append(entry)

        data["languages"] = languages

    # --------------------------
    # CLEANUP
    # --------------------------
    async def close(self):
        if self.browser:
            logging.info("Closing browser...")
            await self.browser.stop()
            logging.info("Browser closed")