# PubMed Fetcher CLI - Approach, Methodology & Results

##  Approach
The goal of this project was to create a CLI tool that fetches and filters PubMed research papers. It identifies papers with at least one author affiliated with non-academic organizations (pharmaceutical/biotech companies) and saves the results to a CSV file.

---

##  Methodology

###  Technology Stack
- **Language:** Python 3
- **APIs:** PubMed API (via Biopython Entrez)
- **CLI Framework:** Typer
- **Data Handling:** Pandas
- **Unit Testing:** unittest & unittest.mock
- **Logging:** Python logging
- **Output Format:** CSV

###  Design
- Modular Code:
  - `fetcher.py` - API calls and filtering logic
  - `cli.py` - Command-line interface
- Heuristic filtering of academic authors using keywords:
  - “university”, “institute”, “college”, etc.
- Mocked API calls in tests for reliability
- CLI Options:
  - `-f / --file`: Save results as CSV
  - `-d / --debug`: Enable debug logs
  - `-h / --help`: Show usage

---

##  Results
The CLI fetches PubMed papers based on user queries, filters academic authors, and outputs a CSV file.

###  Example Output (results.csv)

| PubmedID  | Title                  | Non-academic Author(s) | Company Affiliation(s)    |
|-----------|------------------------|-------------------------|----------------------------|
| 12345678  | A Study on COVID-19    | John Doe                | Pfizer Inc.                |
| 23456789  | Cancer Immunotherapy   | Jane Smith              | Moderna Therapeutics       |

---

##  Bonus Features
- Typed Python (`typing` used throughout)
- Unit tests with mocked API calls
- Professional project structure (ready for packaging)
- Supports large queries efficiently

---

##  Repository Link
[GitHub Repo: PubMed Fetcher CLI](https://github.com/AkashBalagaon/pharma-paper-fetcher)
