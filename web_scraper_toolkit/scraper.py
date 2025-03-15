"""
Core scraper class for the Web Scraper Toolkit.
"""

import logging
import time
from typing import Dict, List, Any, Optional, Union, Callable
import os
import json

from .config import ScraperConfig
from .engines import get_engine
from .exporters import get_exporter
from .monitoring.logger import setup_logger
from .utils.robots_txt import RobotsTxtChecker

logger = logging.getLogger(__name__)

class Scraper:
    """
    Main scraper class that orchestrates the scraping process.
    
    This class provides a high-level interface for scraping websites using
    different engines (Selenium, BeautifulSoup, Scrapy, Playwright) and
    exporting the data to various formats.
    
    Attributes:
        config (ScraperConfig): Configuration for the scraper.
        engine: The scraping engine instance.
    """
    
    def __init__(self, engine: str = "requests", config: Optional[ScraperConfig] = None):
        """
        Initialize the scraper with the specified engine and configuration.
        
        Args:
            engine (str): The scraping engine to use. Options: "requests", "selenium", 
                         "bs4", "scrapy", "playwright". Default is "requests".
            config (ScraperConfig, optional): Configuration for the scraper. If not provided,
                                             a default configuration will be used.
        """
        # Set up logging
        setup_logger()
        
        # Initialize configuration
        self.config = config or ScraperConfig()
        if engine and engine != self.config.engine:
            self.config.engine = engine
        
        logger.info(f"Initializing scraper with {self.config.engine} engine")
        
        # Initialize the engine
        self.engine = get_engine(self.config.engine, self.config)
        
        # Initialize robots.txt checker if needed
        self.robots_checker = None
        if self.config.respect_robots_txt:
            self.robots_checker = RobotsTxtChecker(self.config.user_agent)
            logger.info("Robots.txt checking enabled")
    
    def scrape(self, url: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scrape data from a single URL using the provided schema.
        
        Args:
            url (str): The URL to scrape.
            schema (Dict[str, Any]): The schema defining what data to extract.
                Example:
                {
                    "title": "h1",  # Simple selector
                    "paragraphs": "p",  # Multiple elements
                    "links": {"selector": "a", "attribute": "href"},  # With attribute
                    "date": {"selector": ".date", "processors": [date_processor]}  # With processor
                }
        
        Returns:
            Dict[str, Any]: The scraped data.
        """
        logger.info(f"Scraping URL: {url}")
        
        # Check robots.txt if enabled
        if self.robots_checker and not self.robots_checker.can_fetch(url):
            logger.warning(f"Robots.txt disallows scraping {url}")
            return {}
        
        # Apply request delay if configured
        if self.config.request_delay > 0:
            logger.debug(f"Applying request delay of {self.config.request_delay} seconds")
            time.sleep(self.config.request_delay)
        
        # Scrape the URL
        try:
            result = self.engine.scrape(url, schema)
            logger.info(f"Successfully scraped {url}")
            return result
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return {}
    
    def scrape_multiple(self, urls: List[str], schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Scrape data from multiple URLs using the provided schema.
        
        Args:
            urls (List[str]): The URLs to scrape.
            schema (Dict[str, Any]): The schema defining what data to extract.
        
        Returns:
            List[Dict[str, Any]]: The scraped data for each URL.
        """
        logger.info(f"Scraping {len(urls)} URLs")
        
        results = []
        for url in urls:
            result = self.scrape(url, schema)
            if result:
                result["url"] = url  # Add the URL to the result
                results.append(result)
        
        logger.info(f"Successfully scraped {len(results)} out of {len(urls)} URLs")
        return results
    
    def export(self, data: Union[Dict[str, Any], List[Dict[str, Any]]], 
              output_path: str, format: str = None) -> bool:
        """
        Export the scraped data to the specified format.
        
        Args:
            data (Union[Dict[str, Any], List[Dict[str, Any]]]): The data to export.
            output_path (str): The path where to save the exported data.
            format (str, optional): The format to export to. If not provided, it will be
                                   inferred from the output_path extension.
        
        Returns:
            bool: True if the export was successful, False otherwise.
        """
        # Determine format from output_path if not provided
        if not format:
            _, ext = os.path.splitext(output_path)
            format = ext[1:] if ext else "json"  # Default to JSON
        
        logger.info(f"Exporting data to {format} format at {output_path}")
        
        # Get the appropriate exporter
        exporter = get_exporter(format)
        
        # Export the data
        try:
            exporter.export(data, output_path)
            logger.info(f"Successfully exported data to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            return False
    
    def close(self):
        """
        Close the scraper and release resources.
        """
        if hasattr(self.engine, 'close'):
            self.engine.close()
        logger.info("Scraper closed")


# Convenience function for quick scraping
def quick_scrape(url: str, selectors: Dict[str, str], output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Quickly scrape a URL with minimal configuration.
    
    Args:
        url (str): The URL to scrape.
        selectors (Dict[str, str]): A dictionary mapping field names to CSS selectors.
        output_path (str, optional): If provided, the scraped data will be saved to this path.
    
    Returns:
        Dict[str, Any]: The scraped data.
    """
    scraper = Scraper()
    result = scraper.scrape(url, selectors)
    
    if output_path:
        scraper.export(result, output_path)
    
    scraper.close()
    return result