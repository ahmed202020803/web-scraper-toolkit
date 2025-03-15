#!/usr/bin/env python3
"""
Basic scraping example using the Web Scraper Toolkit.

This example demonstrates how to scrape a website and export the data to various formats.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web_scraper_toolkit import Scraper, ScraperConfig

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main function."""
    # Create a scraper with default configuration
    scraper = Scraper(engine="requests")
    
    # Define the data schema
    schema = {
        "title": "h1",
        "description": "meta[name='description']",
        "paragraphs": {
            "selector": "p",
            "multiple": True
        },
        "links": {
            "selector": "a",
            "attribute": "href",
            "multiple": True
        },
        "images": {
            "selector": "img",
            "attribute": "src",
            "multiple": True
        }
    }
    
    # Scrape a website
    print("Scraping example.com...")
    data = scraper.scrape("https://example.com", schema)
    
    # Print the scraped data
    print("\nScraped Data:")
    print(f"Title: {data.get('title')}")
    print(f"Description: {data.get('description')}")
    print(f"Number of paragraphs: {len(data.get('paragraphs', []))}")
    print(f"Number of links: {len(data.get('links', []))}")
    print(f"Number of images: {len(data.get('images', []))}")
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Export the data to various formats
    print("\nExporting data...")
    scraper.export(data, "data/example.json")
    scraper.export(data, "data/example.csv")
    
    # Close the scraper
    scraper.close()
    
    print("\nDone!")

def advanced_example():
    """Advanced example with custom configuration."""
    # Create a custom configuration
    config = ScraperConfig(
        engine="requests",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        user_agent_rotation=True,
        respect_robots_txt=True,
        request_delay=2.0,
        max_retries=3,
        timeout=30,
        verify_ssl=True,
        headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
        }
    )
    
    # Create a scraper with the custom configuration
    scraper = Scraper(config=config)
    
    # Define the data schema
    schema = {
        "title": "h1",
        "description": "meta[name='description']",
        "paragraphs": {
            "selector": "p",
            "multiple": True
        },
        "links": {
            "selector": "a",
            "attribute": "href",
            "multiple": True
        },
        "images": {
            "selector": "img",
            "attribute": "src",
            "multiple": True
        }
    }
    
    # Scrape multiple websites
    print("Scraping multiple websites...")
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]
    
    results = scraper.scrape_multiple(urls, schema)
    
    # Print the scraped data
    print("\nScraped Data:")
    for i, result in enumerate(results):
        print(f"\nWebsite {i+1}:")
        print(f"URL: {result.get('url')}")
        print(f"Title: {result.get('title')}")
        print(f"Description: {result.get('description')}")
        print(f"Number of paragraphs: {len(result.get('paragraphs', []))}")
        print(f"Number of links: {len(result.get('links', []))}")
        print(f"Number of images: {len(result.get('images', []))}")
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Export the data to various formats
    print("\nExporting data...")
    scraper.export(results, "data/multiple_examples.json")
    scraper.export(results, "data/multiple_examples.csv")
    
    # Close the scraper
    scraper.close()
    
    print("\nDone!")

if __name__ == "__main__":
    # Run the basic example
    main()
    
    # Run the advanced example
    # advanced_example()