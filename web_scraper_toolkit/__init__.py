"""
Web Scraper Toolkit - A comprehensive toolkit for scraping and analyzing web data
"""

__version__ = "0.1.0"
__author__ = "Web Scraper Toolkit Team"

from .scraper import Scraper
from .config import ScraperConfig
from .scheduler.job import ScraperJob
from .scheduler.scheduler import JobScheduler

__all__ = [
    "Scraper",
    "ScraperConfig",
    "ScraperJob",
    "JobScheduler",
]