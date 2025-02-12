from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
from config import WAIT_TIME, BASE_URL
from utils import clean_text, setup_logging, categorize_event, save_to_csv
import time
import pandas as pd

logger = setup_logging()

class EventScraper:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--start-maximized')
        self.options.page_load_strategy = 'eager'

    def setup_driver(self):
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.options)
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            return driver
        except Exception as e:
            logger.error(f"Error setting up driver: {str(e)}")
            return None

    def scroll_page(self, driver):
        """Scroll to load all events"""
        logger.info("Scrolling page to load all events...")
        scroll_pause = 2
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause)
            
            # Calculate new scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("No more content to load. Scrolling complete.")
                break
            last_height = new_height

    def get_all_event_links(self):
        """Get all event links"""
        driver = None
        event_links = set()
        
        try:
            driver = self.setup_driver()
            if not driver:
                return []

            logger.info("Accessing events page...")
            driver.get(BASE_URL)
            time.sleep(5)
            
            # Scroll to load all events
            self.scroll_page(driver)
            
            # Get page source and parse with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Find all event links (update selector based on your website)
            events = soup.find_all('a', {'class': 'w-full cursor-pointer hover:no-underline'})
            print(f"Number of events found: {len(events)}")
            
            # Extract links
            for event in events:
                link = event.get('href')
                if link:
                    event_links.add(link)
                    print(f"Found event link: {link}")
            
            logger.info(f"Found {len(event_links)} unique event links")
            
        except Exception as e:
            logger.error(f"Error getting event links: {str(e)}")
        
        finally:
            if driver:
                driver.quit()
        
        return list(event_links)

    def get_event_details(self, url):
        """Get details for a single event"""
        driver = None
        try:
            driver = self.setup_driver()
            if not driver:
                return None

            logger.info(f"Scraping event: {url}")
            driver.get(url)
            time.sleep(3)

            # Parse with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            data = {
                'url': url,
                'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Title
            title = soup.find('h1', class_='overflow-hidden overflow-ellipsis text-3xl font-bold leading-snug')
            data['title'] = clean_text(title.text) if title else "Title not found"
            
            # Location
            location = soup.find('div', {'data-testid': 'location-info'})
            data['location'] = clean_text(location.text) if location else "Location not found"
            
            # Date and Time
            datetime_info = soup.find('time')
            data['date_time'] = datetime_info.get('datetime') if datetime_info else "Date/Time not found"
            
            # Description
            desc_elements = soup.find_all('p', class_='mb-4')
            description = "\n".join([clean_text(elem.text) for elem in desc_elements]) if desc_elements else "Description not found"
            data['description'] = description
            
            # Attendees
            attendees_section = soup.find('div', id='attendees')
            if attendees_section:
                attendees_text = attendees_section.find('h2', class_='text-xl font-semibold').text
                attendees_count = attendees_text.split('(')[-1].split(')')[0]
                data['attendees'] = attendees_count
            else:
                data['attendees'] = "Not found"
            
            # Add category based on description
            data['category'] = categorize_event(description)
            
            print(f"Successfully scraped: {data['title']}")
            return data

        except Exception as e:
            logger.error(f"Error scraping event {url}: {str(e)}")
            return None
        
        finally:
            if driver:
                driver.quit()

    def run_scraper(self):
        """Main method to run the scraper"""
        # Get all event links
        event_links = self.get_all_event_links()
        print(f"Found {len(event_links)} events to scrape")
        
        # Scrape each event
        all_events_data = []
        for url in event_links:
            event_data = self.get_event_details(url)
            if event_data:
                all_events_data.append(event_data)
                print(f"Scraped {len(all_events_data)}/{len(event_links)} events")
            time.sleep(2)
        
        # Save data to CSV
        if all_events_data:
            save_to_csv(all_events_data)
        
        return all_events_data