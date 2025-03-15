"""
Configuration handling for the Web Scraper Toolkit.
"""

import os
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

@dataclass
class ScraperConfig:
    """
    Configuration for the scraper.
    
    This class holds all configuration options for the scraper, including
    engine settings, proxy settings, browser settings, rate limiting, etc.
    
    Attributes:
        engine (str): The scraping engine to use.
        browser (str): The browser to use for browser-based engines.
        headless (bool): Whether to run the browser in headless mode.
        user_agent (str): The user agent to use for requests.
        user_agent_rotation (bool): Whether to rotate user agents.
        use_proxies (bool): Whether to use proxies.
        proxy_rotation_policy (str): The policy for rotating proxies.
        respect_robots_txt (bool): Whether to respect robots.txt.
        request_delay (float): Delay between requests in seconds.
        max_requests_per_minute (int): Maximum number of requests per minute.
        max_retries (int): Maximum number of retries for failed requests.
        timeout (int): Request timeout in seconds.
        verify_ssl (bool): Whether to verify SSL certificates.
        cookies (Dict[str, str]): Cookies to include in requests.
        headers (Dict[str, str]): Headers to include in requests.
        solve_captchas (bool): Whether to solve captchas.
        captcha_service (str): The captcha solving service to use.
        captcha_api_key (str): API key for the captcha solving service.
        log_level (str): The log level to use.
        data_dir (str): Directory for storing data.
    """
    
    # Engine settings
    engine: str = "requests"
    
    # Browser settings
    browser: str = "chrome"
    headless: bool = True
    
    # User agent settings
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    user_agent_rotation: bool = False
    user_agent_list_path: str = "./config/user_agents.txt"
    
    # Proxy settings
    use_proxies: bool = False
    proxy_rotation_policy: str = "round-robin"
    proxy_list_path: str = "./config/proxies.txt"
    
    # Rate limiting
    respect_robots_txt: bool = True
    request_delay: float = 2.0
    max_requests_per_minute: int = 30
    
    # Request settings
    max_retries: int = 3
    timeout: int = 30
    verify_ssl: bool = True
    cookies: Dict[str, str] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    
    # Captcha settings
    solve_captchas: bool = False
    captcha_service: str = "2captcha"
    captcha_api_key: str = ""
    
    # General settings
    log_level: str = "INFO"
    data_dir: str = "./data"
    
    def __post_init__(self):
        """
        Initialize the configuration with values from environment variables.
        """
        # Override settings from environment variables
        self._load_from_env()
        
        # Set default headers if not provided
        if not self.headers:
            self.headers = {
                "User-Agent": self.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Cache-Control": "max-age=0",
            }
    
    def _load_from_env(self):
        """
        Load configuration from environment variables.
        """
        # Engine settings
        if os.getenv("ENGINE"):
            self.engine = os.getenv("ENGINE")
        
        # Browser settings
        if os.getenv("BROWSER"):
            self.browser = os.getenv("BROWSER")
        if os.getenv("HEADLESS"):
            self.headless = os.getenv("HEADLESS").lower() in ("true", "1", "yes")
        
        # User agent settings
        if os.getenv("USER_AGENT"):
            self.user_agent = os.getenv("USER_AGENT")
        if os.getenv("USER_AGENT_ROTATION"):
            self.user_agent_rotation = os.getenv("USER_AGENT_ROTATION").lower() in ("true", "1", "yes")
        if os.getenv("USER_AGENT_LIST_PATH"):
            self.user_agent_list_path = os.getenv("USER_AGENT_LIST_PATH")
        
        # Proxy settings
        if os.getenv("USE_PROXIES"):
            self.use_proxies = os.getenv("USE_PROXIES").lower() in ("true", "1", "yes")
        if os.getenv("PROXY_ROTATION_POLICY"):
            self.proxy_rotation_policy = os.getenv("PROXY_ROTATION_POLICY")
        if os.getenv("PROXY_LIST_PATH"):
            self.proxy_list_path = os.getenv("PROXY_LIST_PATH")
        
        # Rate limiting
        if os.getenv("RESPECT_ROBOTS_TXT"):
            self.respect_robots_txt = os.getenv("RESPECT_ROBOTS_TXT").lower() in ("true", "1", "yes")
        if os.getenv("REQUEST_DELAY"):
            self.request_delay = float(os.getenv("REQUEST_DELAY"))
        if os.getenv("MAX_REQUESTS_PER_MINUTE"):
            self.max_requests_per_minute = int(os.getenv("MAX_REQUESTS_PER_MINUTE"))
        
        # Request settings
        if os.getenv("MAX_RETRIES"):
            self.max_retries = int(os.getenv("MAX_RETRIES"))
        if os.getenv("TIMEOUT"):
            self.timeout = int(os.getenv("TIMEOUT"))
        if os.getenv("VERIFY_SSL"):
            self.verify_ssl = os.getenv("VERIFY_SSL").lower() in ("true", "1", "yes")
        
        # Captcha settings
        if os.getenv("SOLVE_CAPTCHAS"):
            self.solve_captchas = os.getenv("SOLVE_CAPTCHAS").lower() in ("true", "1", "yes")
        if os.getenv("CAPTCHA_SERVICE"):
            self.captcha_service = os.getenv("CAPTCHA_SERVICE")
        if os.getenv("CAPTCHA_API_KEY"):
            self.captcha_api_key = os.getenv("CAPTCHA_API_KEY")
        
        # General settings
        if os.getenv("LOG_LEVEL"):
            self.log_level = os.getenv("LOG_LEVEL")
        if os.getenv("DATA_DIR"):
            self.data_dir = os.getenv("DATA_DIR")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the configuration to a dictionary.
        
        Returns:
            Dict[str, Any]: The configuration as a dictionary.
        """
        return {
            "engine": self.engine,
            "browser": self.browser,
            "headless": self.headless,
            "user_agent": self.user_agent,
            "user_agent_rotation": self.user_agent_rotation,
            "user_agent_list_path": self.user_agent_list_path,
            "use_proxies": self.use_proxies,
            "proxy_rotation_policy": self.proxy_rotation_policy,
            "proxy_list_path": self.proxy_list_path,
            "respect_robots_txt": self.respect_robots_txt,
            "request_delay": self.request_delay,
            "max_requests_per_minute": self.max_requests_per_minute,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "verify_ssl": self.verify_ssl,
            "cookies": self.cookies,
            "headers": self.headers,
            "solve_captchas": self.solve_captchas,
            "captcha_service": self.captcha_service,
            "captcha_api_key": self.captcha_api_key,
            "log_level": self.log_level,
            "data_dir": self.data_dir,
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'ScraperConfig':
        """
        Create a configuration from a dictionary.
        
        Args:
            config_dict (Dict[str, Any]): The configuration as a dictionary.
        
        Returns:
            ScraperConfig: The configuration.
        """
        return cls(**config_dict)
    
    @classmethod
    def from_file(cls, file_path: str) -> 'ScraperConfig':
        """
        Create a configuration from a file.
        
        Args:
            file_path (str): Path to the configuration file (JSON or YAML).
        
        Returns:
            ScraperConfig: The configuration.
        """
        import json
        import yaml
        
        _, ext = os.path.splitext(file_path)
        
        with open(file_path, 'r') as f:
            if ext.lower() == '.json':
                config_dict = json.load(f)
            elif ext.lower() in ('.yaml', '.yml'):
                config_dict = yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported file extension: {ext}")
        
        return cls.from_dict(config_dict)
    
    def save_to_file(self, file_path: str) -> None:
        """
        Save the configuration to a file.
        
        Args:
            file_path (str): Path to save the configuration file (JSON or YAML).
        """
        import json
        import yaml
        
        _, ext = os.path.splitext(file_path)
        config_dict = self.to_dict()
        
        with open(file_path, 'w') as f:
            if ext.lower() == '.json':
                json.dump(config_dict, f, indent=2)
            elif ext.lower() in ('.yaml', '.yml'):
                yaml.dump(config_dict, f, default_flow_style=False)
            else:
                raise ValueError(f"Unsupported file extension: {ext}")
        
        logger.info(f"Configuration saved to {file_path}")