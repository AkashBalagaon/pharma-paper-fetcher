from typing import List, Dict
from Bio import Entrez
import pandas as pd
import logging

Entrez.email = "youremail@example.com"  # Replace with your email

logger = logging.getLogger(__name__)


def fetch_pubmed_ids(query: str, max_results: int = 100) -> List[str]:
    logger.info(f"Fetching PubMed IDs for query: {query}")
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]


def fetch_pubmed_details(pubmed_ids: List[str]) -> List[Dict]:
    logger.info(f"Fetching details for {len(pubmed_ids)} PubMed IDs")
    handle = Entrez.efetch(db="pubmed", id=",".join(pubmed_ids), rettype="medline", retmode="text")
    from Bio import Medline
    records = Medline.parse(handle)
    papers = []

    for record in records:
        non_academic_authors = []
        company_affiliations = []

        if "AU" in record and "AD" in record:
            for author, affiliation in zip(record.get("AU", []), record.get("AD", [])):
                if not is_academic(affiliation):
                    non_academic_authors.append(author)
                    company_affiliations.append(affiliation)

        papers.append({
            "PubmedID": record.get("PMID", ""),
            "Title": record.get("TI", ""),
            "Publication Date": record.get("DP", ""),
            "Non-academic Author(s)": "; ".join(non_academic_authors),
            "Company Affiliation(s)": "; ".join(company_affiliations),
            "Corresponding Author Email": record.get("EM", "")
        })

    handle.close()
    return papers


def is_academic(affiliation: str) -> bool:
    keywords = ["university", "college", "institute", "school", "academy", "hospital", "lab"]
    return any(word.lower() in affiliation.lower() for word in keywords)


def save_to_csv(papers: List[Dict], filename: str):
    logger.info(f"Saving results to {filename}")
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
