# Web Scraper Toolkit

A comprehensive toolkit for scraping, processing, and analyzing web data with various tools and utilities.

## 🚀 Features

- **Multiple Scraping Engines**: Support for Requests, BeautifulSoup, Selenium, and more
- **Proxy Management**: Rotate proxies to avoid IP bans and rate limiting
- **Data Extraction**: Extract structured data from various web sources
- **Data Storage**: Export to CSV, JSON, and other formats
- **Rate Limiting**: Respect website robots.txt and implement polite scraping
- **User-Agent Rotation**: Rotate user agents to mimic different browsers
- **Google Colab Support**: Run the toolkit directly in Google Colab notebooks

## 📋 Installation

```bash
# Clone the repository
git clone https://github.com/ahmed202020803/web-scraper-toolkit.git
cd web-scraper-toolkit

# Install dependencies
pip install -r requirements.txt
```

## 🔧 Configuration

Create a `.env` file in the project root with your configuration (see `.env.example` for details).

## 🛠️ Usage

### Basic Usage

```python
from web_scraper_toolkit import Scraper

# Initialize a scraper
scraper = Scraper(engine="requests")

# Scrape a website
data = scraper.scrape("https://example.com", {
    "title": "h1",
    "paragraphs": "p",
    "links": {"selector": "a", "attribute": "href"}
})

# Export the data
scraper.export(data, "example_data.json")
```

## 🌐 Using in Google Colab

You can use the Web Scraper Toolkit directly in Google Colab for quick prototyping and analysis:

1. Open the [web_scraper_toolkit_colab.ipynb](https://github.com/ahmed202020803/web-scraper-toolkit/blob/main/examples/web_scraper_toolkit_colab.ipynb) file
2. Click on "Open in Colab" button at the top of the file (or manually copy the notebook to Colab)
3. Run the cells to set up the environment and start scraping

Alternatively, you can use the following code to set up the toolkit in any Colab notebook:

```python
# Clone the repository and install dependencies
!git clone https://github.com/ahmed202020803/web-scraper-toolkit.git
!cd web-scraper-toolkit && pip install -r requirements.txt

# Add the repository to the Python path
import sys
sys.path.append('/content/web-scraper-toolkit')

# Import the toolkit
from web_scraper_toolkit import Scraper, ScraperConfig

# Create a scraper and start scraping
scraper = Scraper(engine="requests")
data = scraper.scrape("https://example.com", {"title": "h1"})
print(data)
```

## 📁 Project Structure

```
web-scraper-toolkit/
├── config/                  # Configuration files
├── examples/                # Example scripts
│   ├── basic_scraping.py
│   ├── e-commerce_scraper.py
│   └── web_scraper_toolkit_colab.ipynb  # Google Colab notebook
├── web_scraper_toolkit/     # Main package
│   ├── __init__.py
│   ├── config.py            # Configuration handling
│   ├── engines/             # Scraping engines
│   ├── exporters/           # Data exporters
│   └── utils/               # Utility functions
├── .env.example             # Example environment variables
└── requirements.txt         # Python dependencies
```

## 📊 Example Use Cases

1. **E-commerce Price Monitoring**: Track product prices across multiple websites
2. **News Aggregation**: Collect news articles from various sources
3. **Research Data Collection**: Collect data for academic research
4. **Job Listing Aggregation**: Gather job listings from multiple job boards

## 🔒 Legal Considerations

Always ensure you're complying with:
- Website Terms of Service
- robots.txt directives
- Rate limiting and politeness
- Data privacy laws

This toolkit is provided for educational and legitimate research purposes only.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.