from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def get_event_titles():
    # Setup driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        print("Accessing lu.ma/toronto...")
        driver.get('https://lu.ma/toronto')
        time.sleep(5)

        # Wait for events to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h3"))
        )

        # Scroll to load all content
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # Get all event cards
        event_cards = driver.find_elements(By.CSS_SELECTOR, "div[class*='content-card']")
        print(f"\nFound {len(event_cards)} event cards")

        for card in event_cards:
            try:
                # Get title
                title = card.find_element(By.TAG_NAME, "h3").text
                
                # Get parent div with onclick
                onclick = card.get_attribute('onclick')
                
                # Get other details
                time_element = card.find_element(By.CSS_SELECTOR, "span[class*='749509546']").text
                location = card.find_element(By.XPATH, ".//div[contains(text(), 'Toronto') or contains(text(), 'Ontario')]").text
                organizer = card.find_element(By.XPATH, ".//div[contains(text(), 'By ')]").text
                
                print("\nEvent Details:")
                print(f"Title: {title}")
                print(f"Time: {time_element}")
                print(f"Location: {location}")
                print(f"Organizer: {organizer}")
                print(f"Onclick: {onclick}")
                print("-" * 50)

            except Exception as e:
                print(f"Error processing card: {str(e)}")
                continue

    except Exception as e:
        print(f"Error during scraping: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    get_event_titles() 