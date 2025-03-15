"""
Utility functions for the Web Scraper Toolkit.
"""

import logging
import os
import random
import time
from typing import Dict, List, Any, Optional, Union

logger = logging.getLogger(__name__)

def ensure_dir_exists(directory: str) -> None:
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory (str): The directory path.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.debug(f"Created directory: {directory}")

def random_delay(min_seconds: float = 1.0, max_seconds: float = 5.0) -> None:
    """
    Sleep for a random amount of time.
    
    Args:
        min_seconds (float): Minimum sleep time in seconds.
        max_seconds (float): Maximum sleep time in seconds.
    """
    delay = random.uniform(min_seconds, max_seconds)
    logger.debug(f"Sleeping for {delay:.2f} seconds")
    time.sleep(delay)

def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and normalizing.
    
    Args:
        text (str): The text to clean.
    
    Returns:
        str: The cleaned text.
    """
    if not text:
        return ""
    
    # Replace multiple whitespace with a single space
    text = " ".join(text.split())
    
    return text.strip()

def extract_domain(url: str) -> str:
    """
    Extract the domain from a URL.
    
    Args:
        url (str): The URL.
    
    Returns:
        str: The domain.
    """
    from urllib.parse import urlparse
    
    parsed_url = urlparse(url)
    return parsed_url.netloc

def is_valid_url(url: str) -> bool:
    """
    Check if a URL is valid.
    
    Args:
        url (str): The URL to check.
    
    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    import validators
    
    return validators.url(url) is True