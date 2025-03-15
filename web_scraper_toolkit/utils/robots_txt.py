"""
Robots.txt handling for the Web Scraper Toolkit.
"""

import logging
import urllib.robotparser
import urllib.parse
from typing import Dict, Optional
from threading import Lock
import time

logger = logging.getLogger(__name__)

# Cache for robots.txt parsers
_robots_parsers: Dict[str, urllib.robotparser.RobotFileParser] = {}
_robots_parsers_lock = Lock()
_robots_parsers_last_used: Dict[str, float] = {}
_robots_parsers_max_cache_size = 100
_robots_parsers_cache_ttl = 3600  # 1 hour

class RobotsTxtChecker:
    """
    Class for checking if a URL can be fetched according to robots.txt rules.
    """
    
    def __init__(self, user_agent: str):
        """
        Initialize the robots.txt checker.
        
        Args:
            user_agent (str): The user agent to use for checking robots.txt.
        """
        self.user_agent = user_agent
    
    def can_fetch(self, url: str) -> bool:
        """
        Check if a URL can be fetched according to robots.txt rules.
        
        Args:
            url (str): The URL to check.
        
        Returns:
            bool: True if the URL can be fetched, False otherwise.
        """
        # Parse the URL
        parsed_url = urllib.parse.urlparse(url)
        
        # Get the base URL (scheme + netloc)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        # Get the path
        path = parsed_url.path
        if not path:
            path = "/"
        
        # Check if the URL can be fetched
        try:
            parser = self._get_robots_parser(base_url)
            if parser:
                return parser.can_fetch(self.user_agent, path)
            else:
                # If we can't get the robots.txt, assume we can fetch
                return True
        except Exception as e:
            logger.error(f"Error checking robots.txt for {url}: {str(e)}")
            # If there's an error, assume we can fetch
            return True
    
    def _get_robots_parser(self, base_url: str) -> Optional[urllib.robotparser.RobotFileParser]:
        """
        Get a robots.txt parser for a base URL.
        
        Args:
            base_url (str): The base URL (scheme + netloc).
        
        Returns:
            Optional[urllib.robotparser.RobotFileParser]: A robots.txt parser, or None if the robots.txt can't be fetched.
        """
        global _robots_parsers, _robots_parsers_last_used
        
        with _robots_parsers_lock:
            # Clean up old parsers
            self._cleanup_old_parsers()
            
            # Check if we already have a parser for this base URL
            if base_url in _robots_parsers:
                # Update last used time
                _robots_parsers_last_used[base_url] = time.time()
                return _robots_parsers[base_url]
            
            # Create a new parser
            parser = urllib.robotparser.RobotFileParser()
            parser.set_url(f"{base_url}/robots.txt")
            
            try:
                parser.read()
                
                # Cache the parser
                _robots_parsers[base_url] = parser
                _robots_parsers_last_used[base_url] = time.time()
                
                return parser
            except Exception as e:
                logger.error(f"Error reading robots.txt for {base_url}: {str(e)}")
                return None
    
    def _cleanup_old_parsers(self) -> None:
        """
        Clean up old robots.txt parsers from the cache.
        """
        global _robots_parsers, _robots_parsers_last_used, _robots_parsers_max_cache_size, _robots_parsers_cache_ttl
        
        # Check if we need to clean up
        if len(_robots_parsers) <= _robots_parsers_max_cache_size:
            return
        
        # Get current time
        current_time = time.time()
        
        # Remove old parsers
        for base_url in list(_robots_parsers.keys()):
            last_used = _robots_parsers_last_used.get(base_url, 0)
            if current_time - last_used > _robots_parsers_cache_ttl:
                del _robots_parsers[base_url]
                del _robots_parsers_last_used[base_url]
        
        # If we still have too many parsers, remove the oldest ones
        if len(_robots_parsers) > _robots_parsers_max_cache_size:
            # Sort by last used time
            sorted_urls = sorted(_robots_parsers_last_used.items(), key=lambda x: x[1])
            
            # Remove the oldest ones
            for base_url, _ in sorted_urls[:len(_robots_parsers) - _robots_parsers_max_cache_size]:
                del _robots_parsers[base_url]
                del _robots_parsers_last_used[base_url]

def get_crawl_delay(url: str, user_agent: str) -> Optional[float]:
    """
    Get the crawl delay for a URL from robots.txt.
    
    Args:
        url (str): The URL to check.
        user_agent (str): The user agent to use for checking robots.txt.
    
    Returns:
        Optional[float]: The crawl delay in seconds, or None if not specified.
    """
    # Parse the URL
    parsed_url = urllib.parse.urlparse(url)
    
    # Get the base URL (scheme + netloc)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    # Create a parser
    parser = urllib.robotparser.RobotFileParser()
    parser.set_url(f"{base_url}/robots.txt")
    
    try:
        parser.read()
        return parser.crawl_delay(user_agent)
    except Exception as e:
        logger.error(f"Error reading robots.txt for {base_url}: {str(e)}")
        return None

def get_request_rate(url: str, user_agent: str) -> Optional[tuple]:
    """
    Get the request rate for a URL from robots.txt.
    
    Args:
        url (str): The URL to check.
        user_agent (str): The user agent to use for checking robots.txt.
    
    Returns:
        Optional[tuple]: A tuple of (requests, seconds), or None if not specified.
    """
    # Parse the URL
    parsed_url = urllib.parse.urlparse(url)
    
    # Get the base URL (scheme + netloc)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    # Create a parser
    parser = urllib.robotparser.RobotFileParser()
    parser.set_url(f"{base_url}/robots.txt")
    
    try:
        parser.read()
        return parser.request_rate(user_agent)
    except Exception as e:
        logger.error(f"Error reading robots.txt for {base_url}: {str(e)}")
        return None

def get_sitemaps(url: str) -> list:
    """
    Get the sitemaps for a URL from robots.txt.
    
    Args:
        url (str): The URL to check.
    
    Returns:
        list: A list of sitemap URLs, or an empty list if none are specified.
    """
    # Parse the URL
    parsed_url = urllib.parse.urlparse(url)
    
    # Get the base URL (scheme + netloc)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    # Create a parser
    parser = urllib.robotparser.RobotFileParser()
    parser.set_url(f"{base_url}/robots.txt")
    
    try:
        parser.read()
        return parser.site_maps()
    except Exception as e:
        logger.error(f"Error reading robots.txt for {base_url}: {str(e)}")
        return []