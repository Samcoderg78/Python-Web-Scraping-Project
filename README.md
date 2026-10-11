# Python Web Scraping Project

A Python-based web scraper that extracts product information from [MDComputers](https://mdcomputers.in/) using **Requests** and **Beautiful Soup**. The scraper supports multiple search keywords, pagination, duplicate detection, and exporting structured data to CSV or JSON.

## Features

- **Multi-keyword search:** Search for multiple product terms in a single execution.
- **Product information extraction:** Collect product names, URLs, list prices, and current prices.
- **Pagination support:** Scrape multiple pages of search results, subject to a configurable page limit.
- **Duplicate detection:** Avoid duplicate product URLs across different search terms.
- **Multiple output formats:** Export results as JSON or CSV.
- **HTTP error handling:** Handle request failures and timeouts.
- **Command-line interface:** Specify search terms and output formats directly from the terminal.

## Tech Stack

- Python
- Requests
- Beautiful Soup 4
- HTML parsing
- CSV and JSON

## Project Structure

```text
Python-Web-Scraping-Project/
├── q1_scraper.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Prerequisites

- Python 3.9 or later
- pip
- Internet connectivity

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Samcoderg78/Python-Web-Scraping-Project.git
cd Python-Web-Scraping-Project
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, create it with:

```text
requests
beautifulsoup4
```

Then run the installation command again.

## Usage

Run the scraper from your terminal using one or more search terms.

### Search for a single product category

```bash
python q1_scraper.py "external harddrive"
```

### Search for multiple product categories

```bash
python q1_scraper.py "external harddrive" "gaming keyboard" "gaming mouse"
```

By default, the scraper prints the combined results in JSON format.

### Export results to CSV

```bash
python q1_scraper.py "external harddrive" "gaming keyboard" --format csv > products.csv
```

### Export results to JSON

```bash
python q1_scraper.py "external harddrive" "gaming keyboard" > products.json
```

## Data Fields

Each extracted product contains the following fields:

| Field | Description |
|---|---|
| `search_term` | Search term that first discovered the product |
| `name` | Product name |
| `url` | Absolute product URL |
| `list_price` | Original/list price, when detected |
| `price` | Current price, when detected |

Prices may be `null` when they cannot be extracted reliably from the available HTML.

## How It Works

1. **Request:** Sends an HTTP GET request to the website's product search endpoint.
2. **Parse:** Uses Beautiful Soup to parse the returned HTML.
3. **Extract:** Finds product listings and extracts names, links, and prices.
4. **Paginate:** Processes successive search-result pages up to the configured limit.
5. **Deduplicate:** Tracks product URLs to avoid repeated records across searches.
6. **Export:** Serializes the results to JSON or CSV.

## Configuration

The following constants can be adjusted in `q1_scraper.py`:

```python
MAX_PAGES = 20
```

This limits the number of result pages processed per search term.

The request timeout and HTTP headers can also be adjusted to suit the target website's requirements.

## Error Handling and Limitations

- HTTP request errors are reported to the terminal.
- The scraper uses a timeout to avoid waiting indefinitely for a response.
- HTML selectors and price extraction rules depend on the website's current page structure.
- Some product listings may not contain detectable prices.
- Duplicate detection is based on product URLs.
- The scraper may stop when a page produces no new product URLs.
- Website changes, rate limits, or access restrictions may affect results.

Always review the website's terms of service and applicable policies before scraping. Use reasonable request rates and do not bypass access controls.

## Future Improvements

Potential enhancements include:

- Stronger data validation and cleaning
- Improved logging and retry mechanisms
- Automated tests for extraction and pagination
- Database storage using PostgreSQL
- Incremental data ingestion
- Scheduled execution
- Integration with cloud storage and analytics tools

## Learning Outcomes

This project demonstrates practical experience with:

- HTTP requests and HTML parsing
- Extracting structured data from websites
- Command-line application development
- Pagination and deduplication
- Error handling
- CSV and JSON data serialization

It also provides a foundation for developing more robust **web data ingestion and ETL pipelines**.

## Author

**Saurabh Yadav**

- GitHub: [@Samcoderg78](https://github.com/Samcoderg78)
- LinkedIn: [Saurabh Yadav](https://www.linkedin.com/in/saurabh-yadav-6zd/)

---

*This project was developed for learning and educational purposes.*
