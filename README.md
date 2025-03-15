# Web Scraper Toolkit

A comprehensive toolkit for scraping, processing, and analyzing web data with various tools and utilities.

## 🚀 Features

- **Multiple Scraping Engines**: Support for Selenium, BeautifulSoup, Scrapy, and Playwright
- **Proxy Management**: Rotate proxies to avoid IP bans and rate limiting
- **Data Extraction**: Extract structured data from HTML, JSON, XML, and JavaScript-rendered pages
- **Data Processing**: Clean, transform, and normalize scraped data
- **Data Storage**: Export to CSV, JSON, Excel, or databases (SQLite, PostgreSQL, MongoDB)
- **Scheduling**: Schedule scraping jobs at regular intervals
- **Monitoring**: Monitor scraping jobs and receive notifications
- **Rate Limiting**: Respect website robots.txt and implement polite scraping
- **Captcha Handling**: Solve common captchas and anti-bot challenges
- **User-Agent Rotation**: Rotate user agents to mimic different browsers
- **Headless Browsing**: Support for headless Chrome and Firefox
- **API Integration**: Extract data from REST and GraphQL APIs
- **Parallel Processing**: Scrape multiple pages simultaneously
- **Error Handling**: Robust error handling and retry mechanisms
- **Logging**: Comprehensive logging for debugging and auditing

## 📋 Installation

```bash
# Clone the repository
git clone https://github.com/ahmed202020803/web-scraper-toolkit.git
cd web-scraper-toolkit

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install browser drivers (for Selenium)
python scripts/install_drivers.py
```

## 🔧 Configuration

Create a `.env` file in the project root with your configuration:

```
# General settings
LOG_LEVEL=INFO
DATA_DIR=./data

# Database settings
DB_TYPE=sqlite  # sqlite, postgres, mongodb
DB_PATH=./data/scraper.db  # For SQLite
# DB_HOST=localhost  # For PostgreSQL/MongoDB
# DB_PORT=5432  # For PostgreSQL/MongoDB
# DB_USER=user  # For PostgreSQL/MongoDB
# DB_PASSWORD=password  # For PostgreSQL/MongoDB
# DB_NAME=scraper  # For PostgreSQL/MongoDB

# Proxy settings
USE_PROXIES=false
PROXY_LIST_PATH=./config/proxies.txt
PROXY_ROTATION_POLICY=round-robin  # round-robin, random

# Browser settings
BROWSER_TYPE=chrome  # chrome, firefox
HEADLESS=true
USER_AGENT_ROTATION=true
USER_AGENT_LIST_PATH=./config/user_agents.txt

# Rate limiting
RESPECT_ROBOTS_TXT=true
REQUEST_DELAY=2  # seconds between requests
MAX_REQUESTS_PER_MINUTE=30

# Captcha settings
SOLVE_CAPTCHAS=false
# CAPTCHA_SERVICE=2captcha  # 2captcha, anticaptcha
# CAPTCHA_API_KEY=your_api_key
```

## 🛠️ Usage

### Basic Usage

```python
from web_scraper_toolkit import Scraper

# Initialize a scraper
scraper = Scraper(engine="selenium")

# Scrape a website
data = scraper.scrape("https://example.com", {
    "title": "h1",
    "paragraphs": "p",
    "links": {"selector": "a", "attribute": "href"}
})

# Export the data
scraper.export(data, "example_data.json")
```

### Advanced Usage

```python
from web_scraper_toolkit import Scraper, ScraperConfig
from web_scraper_toolkit.processors import TextCleaner, DateNormalizer
from web_scraper_toolkit.exporters import PostgreSQLExporter

# Configure the scraper
config = ScraperConfig(
    engine="playwright",
    browser="firefox",
    headless=True,
    use_proxies=True,
    proxy_rotation_policy="random",
    respect_robots_txt=True,
    request_delay=3,
    max_retries=5
)

# Initialize the scraper with the configuration
scraper = Scraper(config=config)

# Define data processors
processors = [
    TextCleaner(remove_html=True, lowercase=False),
    DateNormalizer(format="%Y-%m-%d")
]

# Define the data schema
schema = {
    "title": {"selector": "h1", "processors": [processors[0]]},
    "date": {"selector": ".date", "processors": [processors[0], processors[1]]},
    "content": {"selector": ".content", "processors": [processors[0]]},
    "categories": {"selector": ".category", "multiple": True},
    "image_urls": {"selector": "img", "attribute": "src", "multiple": True}
}

# Scrape multiple pages
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
]

# Scrape with the schema
results = scraper.scrape_multiple(urls, schema)

# Export to PostgreSQL
exporter = PostgreSQLExporter(
    host="localhost",
    port=5432,
    user="user",
    password="password",
    database="scraper"
)
exporter.export(results, "scraped_data")
```

### Scheduling Jobs

```python
from web_scraper_toolkit import ScraperJob, JobScheduler

# Define a job
job = ScraperJob(
    name="Daily News Scraper",
    url="https://news-site.com",
    schema={
        "headlines": {"selector": ".headline", "multiple": True},
        "summaries": {"selector": ".summary", "multiple": True}
    },
    exporter="json",
    export_path="./data/daily_news.json"
)

# Create a scheduler
scheduler = JobScheduler()

# Add the job to run daily at 8:00 AM
scheduler.add_job(job, "daily", "08:00")

# Start the scheduler
scheduler.start()
```

## 📁 Project Structure

```
web-scraper-toolkit/
├── config/                  # Configuration files
│   ├── proxies.txt          # List of proxy servers
│   └── user_agents.txt      # List of user agents
├── data/                    # Directory for storing scraped data
├── docs/                    # Documentation
├── examples/                # Example scripts
│   ├── basic_scraping.py
│   ├── api_scraping.py
│   ├── e-commerce_scraper.py
│   └── news_aggregator.py
├── scripts/                 # Utility scripts
│   └── install_drivers.py   # Script to install browser drivers
├── tests/                   # Test suite
├── web_scraper_toolkit/     # Main package
│   ├── __init__.py
│   ├── scraper.py           # Core scraper class
│   ├── config.py            # Configuration handling
│   ├── engines/             # Scraping engines
│   │   ├── __init__.py
│   │   ├── selenium_engine.py
│   │   ├── bs4_engine.py
│   │   ├── scrapy_engine.py
│   │   └── playwright_engine.py
│   ├── processors/          # Data processors
│   │   ├── __init__.py
│   │   ├── text_processors.py
│   │   ├── date_processors.py
│   │   └── image_processors.py
│   ├── exporters/           # Data exporters
│   │   ├── __init__.py
│   │   ├── csv_exporter.py
│   │   ├── json_exporter.py
│   │   ├── excel_exporter.py
│   │   ├── sqlite_exporter.py
│   │   ├── postgres_exporter.py
│   │   └── mongodb_exporter.py
│   ├── utils/               # Utility functions
│   │   ├── __init__.py
│   │   ├── proxy_manager.py
│   │   ├── user_agent_manager.py
│   │   ├── robots_txt.py
│   │   └── captcha_solver.py
│   ├── scheduler/           # Job scheduling
│   │   ├── __init__.py
│   │   ├── job.py
│   │   └── scheduler.py
│   └── monitoring/          # Monitoring and notifications
│       ├── __init__.py
│       ├── logger.py
│       └── notifier.py
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore file
├── LICENSE                  # License file
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies
```

## 📊 Example Use Cases

1. **E-commerce Price Monitoring**: Track product prices across multiple websites
2. **News Aggregation**: Collect news articles from various sources
3. **Social Media Analysis**: Gather data from social media platforms
4. **Research Data Collection**: Collect data for academic research
5. **Job Listing Aggregation**: Gather job listings from multiple job boards
6. **Real Estate Data Collection**: Track property listings and prices
7. **Weather Data Collection**: Gather weather data from multiple sources
8. **Financial Data Analysis**: Collect stock prices and financial news

## 🔒 Legal Considerations

Always ensure you're complying with:
- Website Terms of Service
- robots.txt directives
- Rate limiting and politeness
- Data privacy laws (GDPR, CCPA, etc.)
- Copyright and intellectual property laws

This toolkit is provided for educational and legitimate research purposes only.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.