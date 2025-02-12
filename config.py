# Scraping configuration
BASE_URL = "https://www.meetup.com/find/?location=ca--on--Toronto&source=EVENTS"
WAIT_TIME = 10
MAX_RETRIES = 3

# Output configuration
OUTPUT_FILE = 'event_details.csv'
LOG_FILE = 'scraper.log'

# Browser configuration
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'