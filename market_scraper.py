# Description: This file contains the code for Passivebot's Facebook Marketplace Scraper API.
# Date: 2024-06-14
# Author: Truong Pham
# Version: 1.0.0.
# Usage: python app.py

from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import re
                 
def crawl_marketplace(city: str, query: str, max_price: int):

    # Load environment variables from the .env file (if present)
    load_dotenv()
    EMAIL = os.getenv('EMAIL')
    PASSWORD = os.getenv('PASSWORD')

    # Define the URL to scrape.
    marketplace_url = f'https://www.facebook.com/marketplace/{city}/search/?query={query}&maxPrice={max_price}'
    initial_url = "https://www.facebook.com/login/device-based/regular/login/"
    # Get listings of particular item in a particular city for a particular price.
    # Initialize the session using Playwright.
    with sync_playwright() as p:
        # Open a new browser page.
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        # Navigate to the URL.
        page.goto(initial_url)
        # Wait for the page to load.
        time.sleep(2)
        try:
            page.wait_for_selector('input[name="email"]').fill(EMAIL)
            page.wait_for_selector('input[name="pass"]').fill(PASSWORD)
            time.sleep(2)
            page.wait_for_selector('button[name="login"]').click()
            time.sleep(2)
            page.goto(marketplace_url)
        except:
            page.goto(marketplace_url)
        # Wait for the page to load.
        time.sleep(2)
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        parsed = []
        listings = soup.find_all('div', class_='x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24')
        for listing in listings:
            try:
                # Get the item image.
                image = listing.find('img', class_='xt7dq6l xl1xv1r x6ikm8r x10wlt62 xh8yej3')['src']
                # Get the item title from span.
                title = listing.find('span', 'x1lliihq x6ikm8r x10wlt62 x1n2onr6').text
                # Get the item price.
                price = listing.find('span', 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u').text
                # Get the item mileage
                mileage = listing.find('span', 'x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84').text
                # Get the item URL.
                post_url = listing.find('a', class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv')['href']
                # Get the item location.
                location = listing.find('span', 'x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84').text
                # Append the parsed data to the list.
                parsed.append({
                    'image': image,
                    'title': title,
                    'price': price,
                    'post_url': post_url,
                    'location': location
                })
            except:
                pass
        # Close the browser.
        browser.close()

        result = []
        for item in parsed:

            # Clean up the facebook link using regex
            pattern = r"/marketplace/item/\d+/"
            clean_link = re.search(pattern, item['post_url'])
            clean_link = "https://www.facebook.com" + clean_link.group()
            # Return the parsed data as a JSON.
            result.append({
                'name': item['title'],
                'price': item['price'],
                'location': item['location'],
                'title': item['title'],
                'image': item['image'],
                'link': clean_link
            })
        return result
