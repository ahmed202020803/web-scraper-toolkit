"""
Proxy management for the Web Scraper Toolkit.
"""

import logging
import random
import os
import time
from typing import List, Optional, Dict, Any
import requests
from threading import Lock

logger = logging.getLogger(__name__)

# Cache for proxies
_proxies_cache: Optional[List[str]] = None
_proxies_lock = Lock()
_current_proxy_index = 0

def _load_proxies(file_path: str) -> List[str]:
    """
    Load proxies from a file.
    
    Args:
        file_path (str): Path to the file containing proxies.
    
    Returns:
        List[str]: List of proxies.
    """
    global _proxies_cache
    
    with _proxies_lock:
        # Return cached proxies if available
        if _proxies_cache is not None:
            return _proxies_cache
        
        # Check if file exists
        if not os.path.exists(file_path):
            logger.warning(f"Proxy file not found: {file_path}")
            return []
        
        # Load proxies from file
        try:
            with open(file_path, "r") as f:
                proxies = [line.strip() for line in f if line.strip()]
            
            if not proxies:
                logger.warning(f"No proxies found in {file_path}")
                return []
            
            # Cache proxies
            _proxies_cache = proxies
            
            logger.info(f"Loaded {len(proxies)} proxies from {file_path}")
            return proxies
        except Exception as e:
            logger.error(f"Error loading proxies from {file_path}: {str(e)}")
            return []

def get_proxy(file_path: str, rotation_policy: str = "round-robin") -> Optional[str]:
    """
    Get a proxy based on the rotation policy.
    
    Args:
        file_path (str): Path to the file containing proxies.
        rotation_policy (str): The proxy rotation policy. Options: "round-robin", "random".
    
    Returns:
        Optional[str]: A proxy, or None if no proxies are available.
    """
    global _current_proxy_index
    
    # Load proxies
    proxies = _load_proxies(file_path)
    
    if not proxies:
        return None
    
    # Get proxy based on rotation policy
    with _proxies_lock:
        if rotation_policy == "random":
            return random.choice(proxies)
        elif rotation_policy == "round-robin":
            proxy = proxies[_current_proxy_index]
            _current_proxy_index = (_current_proxy_index + 1) % len(proxies)
            return proxy
        else:
            logger.warning(f"Unknown proxy rotation policy: {rotation_policy}")
            return random.choice(proxies)

def test_proxy(proxy: str, timeout: int = 5) -> bool:
    """
    Test if a proxy is working.
    
    Args:
        proxy (str): The proxy to test.
        timeout (int): Timeout in seconds.
    
    Returns:
        bool: True if the proxy is working, False otherwise.
    """
    try:
        # Test proxy with a request to a reliable service
        response = requests.get(
            "https://httpbin.org/ip",
            proxies={"http": proxy, "https": proxy},
            timeout=timeout
        )
        
        # Check if the response is valid
        if response.status_code == 200:
            return True
        else:
            logger.warning(f"Proxy {proxy} returned status code {response.status_code}")
            return False
    except Exception as e:
        logger.warning(f"Proxy {proxy} test failed: {str(e)}")
        return False

def filter_working_proxies(proxies: List[str], timeout: int = 5, max_workers: int = 10) -> List[str]:
    """
    Filter out non-working proxies.
    
    Args:
        proxies (List[str]): List of proxies to test.
        timeout (int): Timeout in seconds for each proxy test.
        max_workers (int): Maximum number of concurrent workers.
    
    Returns:
        List[str]: List of working proxies.
    """
    from concurrent.futures import ThreadPoolExecutor
    
    logger.info(f"Testing {len(proxies)} proxies...")
    
    working_proxies = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all proxy tests
        future_to_proxy = {executor.submit(test_proxy, proxy, timeout): proxy for proxy in proxies}
        
        # Process results as they complete
        for future in future_to_proxy:
            proxy = future_to_proxy[future]
            try:
                if future.result():
                    working_proxies.append(proxy)
            except Exception as e:
                logger.error(f"Error testing proxy {proxy}: {str(e)}")
    
    logger.info(f"Found {len(working_proxies)} working proxies out of {len(proxies)}")
    
    return working_proxies

def refresh_proxies(file_path: str, timeout: int = 5, max_workers: int = 10) -> None:
    """
    Refresh the proxy cache by testing all proxies and updating the cache.
    
    Args:
        file_path (str): Path to the file containing proxies.
        timeout (int): Timeout in seconds for each proxy test.
        max_workers (int): Maximum number of concurrent workers.
    """
    global _proxies_cache
    
    # Load proxies
    proxies = _load_proxies(file_path)
    
    if not proxies:
        return
    
    # Test proxies
    working_proxies = filter_working_proxies(proxies, timeout, max_workers)
    
    # Update cache
    with _proxies_lock:
        _proxies_cache = working_proxies
    
    logger.info(f"Proxy cache refreshed with {len(working_proxies)} working proxies")

def add_proxy(file_path: str, proxy: str) -> None:
    """
    Add a proxy to the proxy file.
    
    Args:
        file_path (str): Path to the file containing proxies.
        proxy (str): The proxy to add.
    """
    global _proxies_cache
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Check if proxy is already in the file
    proxies = _load_proxies(file_path)
    
    if proxy in proxies:
        logger.info(f"Proxy {proxy} already exists in {file_path}")
        return
    
    # Add proxy to file
    try:
        with open(file_path, "a") as f:
            f.write(f"{proxy}\n")
        
        # Update cache
        with _proxies_lock:
            if _proxies_cache is not None:
                _proxies_cache.append(proxy)
        
        logger.info(f"Added proxy {proxy} to {file_path}")
    except Exception as e:
        logger.error(f"Error adding proxy {proxy} to {file_path}: {str(e)}")

def remove_proxy(file_path: str, proxy: str) -> None:
    """
    Remove a proxy from the proxy file.
    
    Args:
        file_path (str): Path to the file containing proxies.
        proxy (str): The proxy to remove.
    """
    global _proxies_cache
    
    # Load proxies
    proxies = _load_proxies(file_path)
    
    if proxy not in proxies:
        logger.info(f"Proxy {proxy} not found in {file_path}")
        return
    
    # Remove proxy from list
    proxies.remove(proxy)
    
    # Write updated list to file
    try:
        with open(file_path, "w") as f:
            for p in proxies:
                f.write(f"{p}\n")
        
        # Update cache
        with _proxies_lock:
            if _proxies_cache is not None:
                _proxies_cache = proxies
        
        logger.info(f"Removed proxy {proxy} from {file_path}")
    except Exception as e:
        logger.error(f"Error removing proxy {proxy} from {file_path}: {str(e)}")

def get_proxy_info(proxy: str) -> Dict[str, Any]:
    """
    Get information about a proxy.
    
    Args:
        proxy (str): The proxy to get information about.
    
    Returns:
        Dict[str, Any]: Information about the proxy.
    """
    try:
        # Get proxy information from a service
        response = requests.get(
            "https://ipinfo.io/json",
            proxies={"http": proxy, "https": proxy},
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.warning(f"Failed to get proxy info for {proxy}: {response.status_code}")
            return {}
    except Exception as e:
        logger.warning(f"Error getting proxy info for {proxy}: {str(e)}")
        return {}