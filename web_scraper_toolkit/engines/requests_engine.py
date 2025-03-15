"""
Requests-based scraping engine for the Web Scraper Toolkit.
"""

import logging
import requests
from typing import Dict, List, Any, Optional, Union
from bs4 import BeautifulSoup
import time
from tenacity import retry, stop_after_attempt, wait_fixed

from . import BaseEngine, register_engine
from ..config import ScraperConfig
from ..utils.user_agent_manager import get_random_user_agent
from ..utils.proxy_manager import get_proxy

logger = logging.getLogger(__name__)

@register_engine("requests")
class RequestsEngine(BaseEngine):
    """
    Scraping engine based on the requests library and BeautifulSoup.
    
    This engine uses the requests library to fetch web pages and BeautifulSoup
    to parse the HTML and extract data.
    """
    
    def __init__(self, config: ScraperConfig):
        """
        Initialize the engine with the specified configuration.
        
        Args:
            config (ScraperConfig): Configuration for the engine.
        """
        super().__init__(config)
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update(config.headers)
        
        # Set cookies if provided
        if config.cookies:
            self.session.cookies.update(config.cookies)
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def _fetch_page(self, url: str) -> str:
        """
        Fetch a web page.
        
        Args:
            url (str): The URL to fetch.
        
        Returns:
            str: The HTML content of the page.
        
        Raises:
            requests.RequestException: If the request fails.
        """
        # Rotate user agent if enabled
        if self.config.user_agent_rotation:
            self.session.headers["User-Agent"] = get_random_user_agent(self.config.user_agent_list_path)
        
        # Get proxy if enabled
        proxies = None
        if self.config.use_proxies:
            proxy = get_proxy(self.config.proxy_list_path, self.config.proxy_rotation_policy)
            if proxy:
                proxies = {
                    "http": proxy,
                    "https": proxy
                }
        
        # Make the request
        response = self.session.get(
            url,
            timeout=self.config.timeout,
            verify=self.config.verify_ssl,
            proxies=proxies
        )
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        return response.text
    
    def _extract_data(self, soup: BeautifulSoup, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract data from a BeautifulSoup object using the provided schema.
        
        Args:
            soup (BeautifulSoup): The BeautifulSoup object.
            schema (Dict[str, Any]): The schema defining what data to extract.
        
        Returns:
            Dict[str, Any]: The extracted data.
        """
        result = {}
        
        for field_name, field_schema in schema.items():
            # Handle simple string selectors
            if isinstance(field_schema, str):
                selector = field_schema
                elements = soup.select(selector)
                
                if elements:
                    # If multiple elements found, get all text
                    if len(elements) > 1:
                        result[field_name] = [element.get_text(strip=True) for element in elements]
                    else:
                        # Single element, get text
                        result[field_name] = elements[0].get_text(strip=True)
                else:
                    result[field_name] = None
            
            # Handle complex schema with selector, attribute, processors, etc.
            elif isinstance(field_schema, dict):
                selector = field_schema.get("selector")
                attribute = field_schema.get("attribute")
                multiple = field_schema.get("multiple", False)
                processors = field_schema.get("processors", [])
                
                if not selector:
                    logger.warning(f"No selector provided for field '{field_name}'")
                    continue
                
                elements = soup.select(selector)
                
                if not elements:
                    result[field_name] = [] if multiple else None
                    continue
                
                # Extract data from elements
                extracted_data = []
                for element in elements:
                    if attribute:
                        # Get attribute value
                        value = element.get(attribute)
                    else:
                        # Get text content
                        value = element.get_text(strip=True)
                    
                    # Apply processors
                    for processor in processors:
                        if value is not None:
                            value = processor(value)
                    
                    extracted_data.append(value)
                
                # Set result based on whether multiple values are expected
                if multiple:
                    result[field_name] = extracted_data
                else:
                    result[field_name] = extracted_data[0] if extracted_data else None
        
        return result
    
    def scrape(self, url: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scrape data from a URL using the provided schema.
        
        Args:
            url (str): The URL to scrape.
            schema (Dict[str, Any]): The schema defining what data to extract.
        
        Returns:
            Dict[str, Any]: The scraped data.
        """
        try:
            # Fetch the page
            html = self._fetch_page(url)
            
            # Parse the HTML
            soup = BeautifulSoup(html, "lxml")
            
            # Extract data
            result = self._extract_data(soup, schema)
            
            return result
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return {}
    
    def close(self):
        """
        Close the engine and release resources.
        """
        self.session.close()
        logger.debug("Requests engine closed")