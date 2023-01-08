from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re


def scraper(link):
    # Using webdriver we can log into Linkedin via Chrome
    driver = webdriver.Chrome("/Users/niyas/Desktop/Projects/Python/Linkedin Scraper/chromedriver")
    driver.get("https://linkedin.com/uas/login")
    time.sleep(3)
    username = driver.find_element_by_id("username")
    username.send_keys(input("Enter your Email Address: "))
    password = driver.find_element_by_id("password")
    password.send_keys(input("Enter your Password: "))
    driver.find_element_by_xpath("//button[@type='submit']").click()

    # Use a test profile, I chose Martha Stewart's profile for simplicity
    driver.get(link)

    # This will let us scroll down to the bottom of the page and wait for everything to load
    start = time.time()
    initialScroll = 0
    finalScroll = 1000
    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        initialScroll = finalScroll
        finalScroll += 1000
        # This sleep time may need to change slightly to load the whole page properly
        time.sleep(3)
        end = time.time()
        if round(end - start) > 20:
            break

    # This creates our LXML file from our profile of interest based on the page source
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # From the intro section, we can find the name of the person
    intro = soup.find('div', {'class': 'pv-text-details__left-panel'})
    name = intro.find("h1").get_text().strip()

    # From the experience section, we can find the person's most recent experience
    most_recent_experience = soup.find_all('div', {'class': 'pvs-list__outer-container'})
    position = most_recent_experience[1].find_all("span")[0].find_all("span")[0].get_text().strip()

    company_block = most_recent_experience[1].find('div', {'class': 'display-flex flex-column full-width'})
    company = company_block.find("span", {'class': 't-14 t-normal'}).find_all("span")[0].get_text().strip()

    # We can also get the time frame of their most recent experience
    time_block = company_block.find("span", {'class': 't-14 t-normal t-black--light'}).find_all("span")[
        0].get_text().strip()
    start_time = re.split("-", time_block)[0]
    start_time_end_Index = time_block.find("-")
    end_time_Index = time_block.find("·")
    end_time = time_block[(start_time_end_Index + 1):end_time_Index]
    total_time = time_block[(end_time_Index + 1):]

    # Final print statement to summarize the data we have found
    data = "This person's name is " + name + " and they work as a " + position + " at " + company + "." \
    "They have worked there from " + start_time + "to" + end_time + "for a total of" + total_time + "."
    return data