"""
User agent management for the Web Scraper Toolkit.
"""

import logging
import random
import os
from typing import List, Optional
from fake_useragent import UserAgent

logger = logging.getLogger(__name__)

# Default user agents
DEFAULT_USER_AGENTS = [
    # Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
    
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux i686; rv:89.0) Gecko/20100101 Firefox/89.0",
    
    # Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    
    # Opera
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.254",
]

# Cache for user agents
_user_agents_cache: Optional[List[str]] = None
_fake_ua: Optional[UserAgent] = None

def _load_user_agents(file_path: str) -> List[str]:
    """
    Load user agents from a file.
    
    Args:
        file_path (str): Path to the file containing user agents.
    
    Returns:
        List[str]: List of user agents.
    """
    global _user_agents_cache
    
    # Return cached user agents if available
    if _user_agents_cache is not None:
        return _user_agents_cache
    
    # Check if file exists
    if not os.path.exists(file_path):
        logger.warning(f"User agent file not found: {file_path}")
        return DEFAULT_USER_AGENTS
    
    # Load user agents from file
    try:
        with open(file_path, "r") as f:
            user_agents = [line.strip() for line in f if line.strip()]
        
        if not user_agents:
            logger.warning(f"No user agents found in {file_path}")
            return DEFAULT_USER_AGENTS
        
        # Cache user agents
        _user_agents_cache = user_agents
        
        logger.info(f"Loaded {len(user_agents)} user agents from {file_path}")
        return user_agents
    except Exception as e:
        logger.error(f"Error loading user agents from {file_path}: {str(e)}")
        return DEFAULT_USER_AGENTS

def get_random_user_agent(file_path: Optional[str] = None) -> str:
    """
    Get a random user agent.
    
    Args:
        file_path (str, optional): Path to the file containing user agents.
    
    Returns:
        str: A random user agent.
    """
    global _fake_ua
    
    # Try to use fake-useragent if file_path is not provided
    if file_path is None:
        try:
            if _fake_ua is None:
                _fake_ua = UserAgent()
            return _fake_ua.random
        except Exception as e:
            logger.warning(f"Error using fake-useragent: {str(e)}")
            return random.choice(DEFAULT_USER_AGENTS)
    
    # Load user agents from file
    user_agents = _load_user_agents(file_path)
    
    # Return a random user agent
    return random.choice(user_agents)

def get_specific_browser_user_agent(browser: str, file_path: Optional[str] = None) -> str:
    """
    Get a user agent for a specific browser.
    
    Args:
        browser (str): The browser name (chrome, firefox, safari, edge, opera).
        file_path (str, optional): Path to the file containing user agents.
    
    Returns:
        str: A user agent for the specified browser.
    """
    global _fake_ua
    
    # Try to use fake-useragent if file_path is not provided
    if file_path is None:
        try:
            if _fake_ua is None:
                _fake_ua = UserAgent()
            
            browser = browser.lower()
            if browser == "chrome":
                return _fake_ua.chrome
            elif browser == "firefox":
                return _fake_ua.firefox
            elif browser == "safari":
                return _fake_ua.safari
            elif browser == "edge":
                return _fake_ua.edge
            elif browser == "opera":
                return _fake_ua.opera
            else:
                return _fake_ua.random
        except Exception as e:
            logger.warning(f"Error using fake-useragent: {str(e)}")
    
    # Load user agents from file
    user_agents = _load_user_agents(file_path)
    
    # Filter user agents by browser
    browser = browser.lower()
    filtered_agents = []
    
    for agent in user_agents:
        agent_lower = agent.lower()
        if browser == "chrome" and "chrome" in agent_lower and "edg" not in agent_lower and "opr" not in agent_lower:
            filtered_agents.append(agent)
        elif browser == "firefox" and "firefox" in agent_lower:
            filtered_agents.append(agent)
        elif browser == "safari" and "safari" in agent_lower and "chrome" not in agent_lower:
            filtered_agents.append(agent)
        elif browser == "edge" and "edg" in agent_lower:
            filtered_agents.append(agent)
        elif browser == "opera" and "opr" in agent_lower:
            filtered_agents.append(agent)
    
    # Return a random user agent for the specified browser
    if filtered_agents:
        return random.choice(filtered_agents)
    else:
        # Fallback to default user agents
        for agent in DEFAULT_USER_AGENTS:
            agent_lower = agent.lower()
            if browser == "chrome" and "chrome" in agent_lower and "edg" not in agent_lower and "opr" not in agent_lower:
                return agent
            elif browser == "firefox" and "firefox" in agent_lower:
                return agent
            elif browser == "safari" and "safari" in agent_lower and "chrome" not in agent_lower:
                return agent
            elif browser == "edge" and "edg" in agent_lower:
                return agent
            elif browser == "opera" and "opr" in agent_lower:
                return agent
        
        # If no matching user agent found, return a random one
        return random.choice(DEFAULT_USER_AGENTS)