"""
Scraping engines for the Web Scraper Toolkit.
"""

import logging
from typing import Dict, Any, Optional, Type

from ..config import ScraperConfig

logger = logging.getLogger(__name__)

class BaseEngine:
    """
    Base class for all scraping engines.
    
    This class defines the interface that all scraping engines must implement.
    """
    
    def __init__(self, config: ScraperConfig):
        """
        Initialize the engine with the specified configuration.
        
        Args:
            config (ScraperConfig): Configuration for the engine.
        """
        self.config = config
    
    def scrape(self, url: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scrape data from a URL using the provided schema.
        
        Args:
            url (str): The URL to scrape.
            schema (Dict[str, Any]): The schema defining what data to extract.
        
        Returns:
            Dict[str, Any]: The scraped data.
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def close(self):
        """
        Close the engine and release resources.
        """
        pass


# Registry of available engines
_engines: Dict[str, Type[BaseEngine]] = {}

def register_engine(name: str):
    """
    Decorator to register an engine.
    
    Args:
        name (str): The name of the engine.
    
    Returns:
        Callable: The decorator function.
    """
    def decorator(cls):
        _engines[name] = cls
        return cls
    return decorator

def get_engine(name: str, config: ScraperConfig) -> BaseEngine:
    """
    Get an instance of the specified engine.
    
    Args:
        name (str): The name of the engine.
        config (ScraperConfig): Configuration for the engine.
    
    Returns:
        BaseEngine: An instance of the specified engine.
    
    Raises:
        ValueError: If the specified engine is not found.
    """
    # Import engines here to avoid circular imports
    from .requests_engine import RequestsEngine
    from .bs4_engine import BeautifulSoupEngine
    from .selenium_engine import SeleniumEngine
    from .playwright_engine import PlaywrightEngine
    from .scrapy_engine import ScrapyEngine
    
    if name not in _engines:
        available_engines = ", ".join(_engines.keys())
        raise ValueError(f"Engine '{name}' not found. Available engines: {available_engines}")
    
    engine_cls = _engines[name]
    return engine_cls(config)