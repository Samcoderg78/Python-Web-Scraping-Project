# Affinity Answers – Data Engineer (Intern) Assignment

## Setup
```bash
pip install -r requirements.txt
```
Q3 needs `gawk` and `curl` (Linux: `sudo apt install gawk curl`; macOS: `brew install gawk`).

## Q1 – Scraper
```bash
python q1_scraper.py "external harddrive"                 # JSON (default)
python q1_scraper.py "external harddrive" --format csv > products.csv
```
Design: `requests` + `BeautifulSoup` (the site is server-rendered, no browser needed);
loops over `&page=N` until no new products appear; JSON keeps structure, CSV opens in Excel.

## Q2 – SQL
`q2_queries.sql` holds the queries; `q2_run.py` runs them against the public Rfam server (no MySQL client needed):
```bash
python q2_run.py
```

## Q3 – Shell
```bash
bash q3_companies.sh https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv
```