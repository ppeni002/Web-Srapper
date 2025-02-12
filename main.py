from scraper import EventScraper
from utils import save_to_csv
import logging

def main():
    # Initialize scraper
    scraper = EventScraper()
    
    # Run the scraper
    events_data = scraper.run_scraper()
    
    # Save the data
    if events_data:
        if save_to_csv(events_data):
            print(f"\nSuccessfully scraped and saved {len(events_data)} events")
            # Print first few events as sample
            print("\nSample of scraped events:")
            for event in events_data[:3]:
                print(f"\nTitle: {event['title']}")
                print(f"Date/Time: {event['date_time']}")
                print(f"Location: {event['location']}")
                print(f"Category: {event['category']}")
        else:
            print("Failed to save events data")
    else:
        print("No events were scraped")

if __name__ == "__main__":
    main() 