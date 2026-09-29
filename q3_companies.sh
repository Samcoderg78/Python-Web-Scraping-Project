#!/usr/bin/env bash
# Q3: Print company name, location and founding year, sorted by founding year.
# Usage: ./q3_companies.sh <csv-url>
# Requires: curl, gawk (FPAT is a gawk feature; needed because some fields are quoted and contain commas)

set -euo pipefail

URL="${1:?Usage: $0 <csv-url>}"

{
  printf 'Company\tLocation\tFounded\n'
  curl -fsSL "$URL" | tr -d '\r' | gawk '
    BEGIN { FPAT = "([^,]*)|(\"[^\"]+\")"; OFS = "\t" }
    NR > 1 {
      for (i = 1; i <= NF; i++) {
        gsub(/^"|"$/, "", $i)          # strip quotes
        gsub(/\[[0-9]+\]/, "", $i)     # strip footnote markers like [2]
      }
      year = match($8, /[0-9]{4}/) ? substr($8, RSTART, 4) : "N/A"  # "1851 (1892)" -> 1851
      print $2, $5, year
    }' | sort -t$'\t' -k3,3 -s
}