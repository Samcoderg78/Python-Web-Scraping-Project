# Affinity Answers – Data Engineer (Intern) Assignment

Solutions for the take-home questions: a Python scraper, SQL queries on the Rfam database, and a Unix shell script.

## Screen recordings

- Q1 – Python scraper: https://drive.google.com/file/d/1I28Do1qiU_nrh_ajn7-WEiNwhCDDAaaz/view?usp=sharing
- Q2 – SQL: https://drive.google.com/file/d/1RoLcNkO9qhz_TKRz5kU3uYwzHPlziS9u/view?usp=sharing
- Q3 – Shell script: https://drive.google.com/file/d/1EnoyE9kGWXkd22iY9tdQ7CWE7AIaWYqx/view?usp=sharing

## Files

| File | Description |
|------|-------------|
| `q1_scraper.py` | Q1: MD Computers product scraper |
| `products.csv` | Q1: sample output |
| `q2_queries.sql` | Q2: SQL queries |
| `q2_run.py` | Q2: runs the queries on the public Rfam server |
| `q3_companies.sh` | Q3: shell script |
| `requirements.txt` | Python dependencies |

## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows (PowerShell); on macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

Q3 also needs `bash`, `curl` and `gawk` (included with Git for Windows).

## Q1 – Python scraper

Takes a search term and extracts each product's name, URL, list price and current price from mdcomputers.in.

```bash
python q1_scraper.py "external harddrive"                       # JSON (default)
python q1_scraper.py "external harddrive" --format csv > products.csv
```

Returns 44 products for "external harddrive", matching the site's count.

**Design choices**
- The product listings are in the HTML sent by the server, so `requests` + `BeautifulSoup` is enough (no browser automation).
- Follows the result pages until no new products appear (max 20 pages as a safety limit).
- JSON by default since it keeps the structure; CSV is available for spreadsheets.
- Includes a User-Agent, timeout, and error handling for failed requests and empty results.

## Q2 – SQL

Queries are in `q2_queries.sql`. `q2_run.py` runs them on the public Rfam database (no MySQL client needed):

```bash
python q2_run.py
```

**Answers**
1. Acacia species in the taxonomy table: **326**
2. Wheat with the longest sequence: ***Triticum durum*** (836,514,780)
3. Page 9 of families (15 per page, longest sequence > 1,000,000): `LIMIT 15 OFFSET 120`

Sample of the page-9 result:

| family_accession | family_name | max_sequence_length |
|------------------|-------------|---------------------|
| RF01219 | snoR100 | 836514780 |
| RF01220 | snoR104 | 836514780 |
| RF01224 | snoR80 | 836514780 |

Many families share the same longest sequence, so `rfam_acc` is used as a tie-breaker to keep the pagination stable.

## Q3 – Shell script

Downloads the CSV from a URL and prints each company's name, location and founding year, sorted by year.

```bash
bash q3_companies.sh https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv
```

I primarily use Windows, so I ran this from PowerShell using `bash`.

Sample output:

```
Company                    Location                  Founded
State Street Corporation   Boston, Massachusetts     1792
Colgate-Palmolive          New York City, New York   1806
Hartford (The)             Hartford, Connecticut     1810
```

`gawk` with `FPAT` is used to parse the CSV, because some quoted fields contain commas.