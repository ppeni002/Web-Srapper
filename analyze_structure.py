from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def analyze_website_structure():
    # Setup driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        print("Accessing lu.ma/toronto...")
        driver.get('https://lu.ma/toronto')
        time.sleep(5)

        # Scroll a bit to load content
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(2)

        # Get one event card's structure
        print("\nAnalyzing event card structure...")
        event_cards = driver.find_elements(By.TAG_NAME, "h3")
        if event_cards:
            sample_card = event_cards[0]
            print("\nSample Event Title:", sample_card.text)
            
            # Get parent elements structure
            current = sample_card
            level = 0
            print("\nParent elements hierarchy:")
            while current:
                try:
                    print(f"\nLevel {level}:")
                    print("Tag:", current.tag_name)
                    print("Class:", current.get_attribute('class'))
                    print("onClick:", current.get_attribute('onclick'))
                    
                    # Try to get the parent
                    current = current.find_element(By.XPATH, '..')
                    level += 1
                except:
                    break

            # Get the entire HTML structure around the event card
            print("\nFull HTML structure around the event card:")
            parent = sample_card.find_element(By.XPATH, '../..')  # Go up two levels
            print(parent.get_attribute('outerHTML'))

            # Look for specific elements
            print("\nSearching for clickable elements:")
            clickable = driver.find_elements(By.CSS_SELECTOR, "[onclick*='window.open']")
            if clickable:
                print(f"Found {len(clickable)} clickable elements")
                print("\nSample clickable element attributes:")
                print("onClick:", clickable[0].get_attribute('onclick'))
                print("Class:", clickable[0].get_attribute('class'))
                print("HTML:", clickable[0].get_attribute('outerHTML'))

    except Exception as e:
        print(f"Error during analysis: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    analyze_website_structure() 