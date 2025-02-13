from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

def get_event_links():
    # Setup driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    event_data = []
    
    try:
        print("Accessing lu.ma/toronto...")
        driver.get('https://lu.ma/toronto')
        time.sleep(5)

        # Wait for events to load and scroll
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            print(f"Scroll {i+1}/3")

        # First, let's print the structure of one event card to understand it better
        print("\nAnalyzing page structure...")
        
        # Find the main container
        main_content = driver.find_element(By.CSS_SELECTOR, "div[class*='jsx-2422347294 events']")
        print("Found main content container")
        
        # Find all event cards
        cards = main_content.find_elements(By.CSS_SELECTOR, "div[class*='content-card']")
        print(f"\nFound {len(cards)} event cards")

        for card in cards:
            try:
                # Print the HTML structure of the first card for analysis
                if len(event_data) == 0:
                    print("\nExample card HTML structure:")
                    print(card.get_attribute('outerHTML')[:500])
                    print("\nCard attributes:")
                    print("Class:", card.get_attribute('class'))
                    print("onclick:", card.get_attribute('onclick'))
                    print("role:", card.get_attribute('role'))
                
                # Get title from h3
                title = card.find_element(By.TAG_NAME, "h3").text
                
                # Get time
                try:
                    time_elem = card.find_element(By.CSS_SELECTOR, "span[class*='749509546']")
                    time_text = time_elem.text
                except:
                    time_text = "N/A"
                
                # Get link from the a tag
                link_elem = card.find_element(By.CSS_SELECTOR, "a.event-link.content-link")
                href = link_elem.get_attribute('href')
                
                event_data.append({
                    'title': title,
                    'time': time_text,
                    'link': href
                })
                
                print(f"\nFound event:")
                print(f"Title: {title}")
                print(f"Time: {time_text}")
                print(f"Link: {href}")
                print("-" * 50)

            except Exception as e:
                print(f"Error processing card: {str(e)}")
                continue

        print(f"\nTotal events found: {len(event_data)}")

        # Save to CSV
        if event_data:
            with open('data/event_links.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['title', 'time', 'link'])
                writer.writeheader()
                writer.writerows(event_data)
            print("Event links saved to data/event_links.csv")

        # If no events found, print more debug info
        if not event_data:
            print("\nDebug: Checking individual elements...")
            # Try to find elements with onclick attributes
            onclick_elements = driver.find_elements(By.CSS_SELECTOR, "[onclick*='window.open']")
            print(f"Found {len(onclick_elements)} elements with onclick attributes")
            if onclick_elements:
                print("\nExample onclick element:")
                print("HTML:", onclick_elements[0].get_attribute('outerHTML'))
                print("onclick:", onclick_elements[0].get_attribute('onclick'))

    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        import traceback
        print(traceback.format_exc())
    finally:
        driver.quit()

    return event_data

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    import os
    if not os.path.exists('data'):
        os.makedirs('data')
        
    get_event_links() 