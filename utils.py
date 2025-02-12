import logging
import pandas as pd
from config import LOG_FILE, OUTPUT_FILE
import re

def setup_logging():
    """Configure logging settings"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers = []
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(console_handler)
    
    return logger

def clean_text(text):
    """Clean and normalize text data"""
    if not text:
        return ""
    # Remove extra whitespace and normalize text
    cleaned = ' '.join(text.strip().split())
    # Remove any non-printable characters
    cleaned = ''.join(char for char in cleaned if char.isprintable())
    return cleaned

def categorize_event(description):
    """Categorize event based on description"""
    description = description.lower()
    
    entertainment_keywords = {
        'music', 'dance', 'movie', 'comedy', 'show', 'concert',
        'art', 'exhibition', 'live', 'festival', 'performance',
        'entertainment', 'party', 'celebration', 'social'
    }
    
    business_keywords = {
        'business', 'conference', 'workshop', 'networking',
        'entrepreneur', 'investor', 'seminar', 'marketing',
        'corporate', 'meeting', 'strategy', 'leadership',
        'professional', 'startup', 'business development'
    }
    
    education_keywords = {
        'education', 'learning', 'training', 'course',
        'class', 'workshop', 'seminar', 'lecture',
        'study', 'academic', 'teaching', 'skills'
    }
    
    # Count keyword matches for each category
    entertainment_count = sum(1 for keyword in entertainment_keywords if keyword in description)
    business_count = sum(1 for keyword in business_keywords if keyword in description)
    education_count = sum(1 for keyword in education_keywords if keyword in description)
    
    # Determine category based on keyword counts
    if business_count > entertainment_count and business_count > education_count:
        return 'Business'
    elif entertainment_count > business_count and entertainment_count > education_count:
        return 'Entertainment'
    elif education_count > business_count and education_count > entertainment_count:
        return 'Education'
    else:
        return 'Other'

def save_to_csv(events_data, filename=OUTPUT_FILE):
    """Save scraped data to CSV file"""
    if not events_data:
        logging.warning("No data to save")
        return False
        
    try:
        df = pd.DataFrame(events_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Data saved to {filename}")
        return True
    except Exception as e:
        logging.error(f"Error saving data: {str(e)}")
        return False

def format_date(date_str):
    """Format date string to consistent format"""
    try:
        # Add your date formatting logic here if needed
        return date_str.strip()
    except:
        return date_str

def format_time(time_str):
    """Format time string to consistent format"""
    try:
        # Add your time formatting logic here if needed
        return time_str.strip()
    except:
        return time_str

def validate_data(data):
    """Validate the scraped data"""
    required_fields = ['title', 'date', 'time', 'location', 'description', 'url']
    
    for field in required_fields:
        if field not in data or not data[field]:
            logging.warning(f"Missing or empty field: {field}")
            data[field] = f"{field} not found"
    
    return data