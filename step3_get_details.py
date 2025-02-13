from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time as time_module
import csv
import pandas as pd

def get_event_details(driver, url):
    driver.get(url)
    time_module.sleep(3)
    
    details = {}
    
    # Get date and time
    try:
        date_div = driver.find_element(By.XPATH, "//div[contains(@class, 'jsx-2370077516 title')]")
        time_div = date_div.find_element(By.XPATH, "following-sibling::div")
        details['date'] = date_div.text
        details['time'] = time_div.text
    except:
        details['date'] = 'N/A'
        details['time'] = 'N/A'
    
    # Get location
    try:
        # Try to get full address first
        location_elements = driver.find_elements(By.XPATH, "//div[contains(text(), 'Register to See Address')]")
        if location_elements:
            # Click to reveal address
            location_elements[0].click()
            time_module.sleep(1)  # Wait for address to load
            
        # Now try to get the full address
        address_elements = driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'location')]//div[contains(@class, 'text-tinted')] | " +
            "//div[contains(@class, 'address')] | " +
            "//div[contains(text(), 'Location')]/following-sibling::div"
        )
        
        full_address = []
        for elem in address_elements:
            text = elem.text.strip()
            if text and text not in ['Location', 'Register to See Address'] and 'Toronto' in text:
                full_address.append(text)
        
        if full_address:
            details['location'] = ' | '.join(full_address)
        else:
            # Fallback to basic location
            location_text = driver.find_element(By.XPATH, "//div[contains(@class, 'jsx-2999812480')]").text
            details['location'] = location_text
    except Exception as e:
        print(f"Location error: {str(e)}")
        details['location'] = 'N/A'
    
    # Get host
    try:
        host_section = driver.find_element(By.XPATH, "//div[contains(text(), 'Hosted By')]/../following-sibling::div")
        details['host'] = host_section.text
    except:
        details['host'] = 'N/A'
    
    # Get attendees
    try:
        going_text = driver.find_element(By.XPATH, "//div[contains(text(), ' Going')]").text
        attendees_text = driver.find_element(By.XPATH, "//div[contains(text(), 'others')]").text
        details['attendees'] = f"{going_text} - {attendees_text}"
    except:
        details['attendees'] = 'N/A'
    
    # Get About Event section
    try:
        about_header = driver.find_element(By.XPATH, "//div[text()='About Event']")
        about_text = ""
        current_element = about_header
        while True:
            try:
                next_element = current_element.find_element(By.XPATH, "following-sibling::div[1]")
                if next_element.text.startswith('Location') or next_element.text == '':
                    break
                about_text += next_element.text + "\n"
                current_element = next_element
            except:
                break
        details['description'] = about_text.strip() if about_text else 'N/A'
    except:
        details['description'] = 'N/A'
    
    return details

def process_all_events():
    # Read the event links
    df = pd.read_csv('data/event_links.csv')
    
    # Setup driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    all_event_details = []
    
    try:
        total_events = len(df)
        for index, row in df.iterrows():
            print(f"\nProcessing event {index + 1}/{total_events}")
            print(f"Title: {row['title']}")
            print(f"URL: {row['link']}")
            
            # Get details for this event
            details = get_event_details(driver, row['link'])
            
            # Add title and link to details
            details['title'] = row['title']
            details['link'] = row['link']
            
            # Add to our list
            all_event_details.append(details)
            
            print("Successfully processed event")
            print("-" * 50)
            
            # Optional: Add a small delay between requests
            time_module.sleep(1)
        
        # Save all details to CSV
        if all_event_details:
            fieldnames = ['title', 'date', 'time', 'location', 'host', 'attendees', 'description', 'link']
            with open('data/event_details.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_event_details)
            print("\nAll event details saved to data/event_details.csv")
            
            # Print summary
            print(f"\nProcessed {len(all_event_details)} events out of {total_events} total")
            
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        import traceback
        print(traceback.format_exc())
    finally:
        driver.quit()

if __name__ == "__main__":
    process_all_events() 