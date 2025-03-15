#!/usr/bin/env python3
"""
E-commerce scraping example using the Web Scraper Toolkit.

This example demonstrates how to scrape product information from e-commerce websites
and monitor prices over time.
"""

import os
import sys
import logging
import time
import json
import datetime
from typing import Dict, List, Any
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

logger = logging.getLogger(__name__)

# Define product URLs to monitor
PRODUCTS = [
    {
        "name": "Example Product 1",
        "url": "https://example.com/product1",
        "selector_schema": {
            "title": "h1.product-title",
            "price": {
                "selector": "span.price",
                "processors": [lambda x: float(x.replace("$", "").replace(",", ""))]
            },
            "availability": "span.availability",
            "rating": {
                "selector": "div.rating",
                "processors": [lambda x: float(x.split("/")[0]) if "/" in x else None]
            },
            "description": "div.product-description",
            "images": {
                "selector": "img.product-image",
                "attribute": "src",
                "multiple": True
            },
            "specifications": {
                "selector": "table.specifications tr",
                "multiple": True,
                "processors": [lambda x: {
                    "name": x.select_one("td:nth-child(1)").text.strip(),
                    "value": x.select_one("td:nth-child(2)").text.strip()
                }]
            }
        }
    },
    # Add more products here
]

def clean_price(price_str: str) -> float:
    """
    Clean a price string and convert it to a float.
    
    Args:
        price_str (str): The price string to clean.
    
    Returns:
        float: The cleaned price as a float.
    """
    # Remove currency symbols and commas
    cleaned = price_str.replace("$", "").replace("€", "").replace("£", "").replace(",", "")
    
    # Extract the first number found
    import re
    match = re.search(r"(\d+\.\d+|\d+)", cleaned)
    if match:
        return float(match.group(1))
    
    return 0.0

def load_price_history(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Load price history from a file.
    
    Args:
        file_path (str): The path to the price history file.
    
    Returns:
        Dict[str, List[Dict[str, Any]]]: The price history.
    """
    if not os.path.exists(file_path):
        return {}
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading price history: {str(e)}")
        return {}

def save_price_history(price_history: Dict[str, List[Dict[str, Any]]], file_path: str) -> None:
    """
    Save price history to a file.
    
    Args:
        price_history (Dict[str, List[Dict[str, Any]]]): The price history.
        file_path (str): The path to save the price history file.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    
    try:
        with open(file_path, 'w') as f:
            json.dump(price_history, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving price history: {str(e)}")

def monitor_prices():
    """Monitor product prices and track changes over time."""
    # Create a scraper with custom configuration
    config = ScraperConfig(
        engine="requests",
        user_agent_rotation=True,
        respect_robots_txt=True,
        request_delay=5.0,  # Be polite with e-commerce sites
        max_retries=3,
        timeout=30
    )
    
    scraper = Scraper(config=config)
    
    # Load existing price history
    price_history_file = "data/price_history.json"
    price_history = load_price_history(price_history_file)
    
    # Current timestamp
    timestamp = datetime.datetime.now().isoformat()
    
    # Scrape each product
    for product in PRODUCTS:
        product_name = product["name"]
        product_url = product["url"]
        selector_schema = product["selector_schema"]
        
        logger.info(f"Scraping product: {product_name}")
        
        try:
            # Scrape the product page
            data = scraper.scrape(product_url, selector_schema)
            
            # Add timestamp and URL
            data["timestamp"] = timestamp
            data["url"] = product_url
            
            # Initialize price history for this product if it doesn't exist
            if product_name not in price_history:
                price_history[product_name] = []
            
            # Add the current price to the history
            price_history[product_name].append({
                "timestamp": timestamp,
                "price": data.get("price"),
                "availability": data.get("availability")
            })
            
            # Check for price changes
            if len(price_history[product_name]) > 1:
                current_price = data.get("price")
                previous_price = price_history[product_name][-2]["price"]
                
                if current_price != previous_price:
                    price_diff = current_price - previous_price
                    percent_change = (price_diff / previous_price) * 100 if previous_price else 0
                    
                    logger.info(f"Price change detected for {product_name}:")
                    logger.info(f"  Previous price: ${previous_price:.2f}")
                    logger.info(f"  Current price: ${current_price:.2f}")
                    logger.info(f"  Difference: ${price_diff:.2f} ({percent_change:.2f}%)")
            
            # Export the current product data
            product_file = f"data/{product_name.lower().replace(' ', '_')}.json"
            scraper.export(data, product_file)
            
        except Exception as e:
            logger.error(f"Error scraping {product_name}: {str(e)}")
    
    # Save the updated price history
    save_price_history(price_history, price_history_file)
    
    # Export a summary of the current prices
    summary = []
    for product_name, history in price_history.items():
        if history:
            latest = history[-1]
            summary.append({
                "product": product_name,
                "price": latest["price"],
                "availability": latest["availability"],
                "timestamp": latest["timestamp"]
            })
    
    scraper.export(summary, "data/price_summary.json")
    scraper.export(summary, "data/price_summary.csv")
    
    # Close the scraper
    scraper.close()

def main():
    """Main function."""
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Run once
    logger.info("Starting e-commerce price monitoring...")
    monitor_prices()
    logger.info("Price monitoring complete.")
    
    # Uncomment to run continuously
    # while True:
    #     logger.info("Starting e-commerce price monitoring...")
    #     monitor_prices()
    #     logger.info("Price monitoring complete. Sleeping for 6 hours...")
    #     time.sleep(6 * 60 * 60)  # Sleep for 6 hours

if __name__ == "__main__":
    main()