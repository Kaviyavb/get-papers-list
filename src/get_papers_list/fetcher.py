import requests
import xml.etree.ElementTree as ET
import pandas as pd
from typing import List


def search_pubmed(query: str, max_results: int = 20) -> List[str]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("esearchresult", {}).get("idlist", [])


def fetch_paper_details(ids: List[str]) -> str:
    id_string = ",".join(ids)
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": id_string,
        "retmode": "xml"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.text


def is_non_academic(affiliation: str) -> bool:
    academic_keywords = ['university', 'institute', 'college', 'hospital', 'school', 'centre', 'center']
    return not any(keyword.lower() in affiliation.lower() for keyword in academic_keywords)


def parse_xml(xml_data: str) -> pd.DataFrame:
    root = ET.fromstring(xml_data)
    records = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date_elem = article.find(".//PubDate")
        if pub_date_elem is not None:
            year = pub_date_elem.findtext("Year") or ""
            month = pub_date_elem.findtext("Month") or ""
            day = pub_date_elem.findtext("Day") or ""
            pub_date = f"{year}-{month}-{day}"
        else:
            pub_date = ""

        non_academic_authors = []
        company_affiliations = []
        email = ""

        for author in article.findall(".//Author"):
            affiliation_info = author.findtext(".//AffiliationInfo/Affiliation")
            if affiliation_info and is_non_academic(affiliation_info):
                last_name = author.findtext("LastName") or ""
                fore_name = author.findtext("ForeName") or ""
                full_name = f"{fore_name} {last_name}".strip()
                non_academic_authors.append(full_name)
                company_affiliations.append(affiliation_info)
                if "@" in affiliation_info:
                    email = affiliation_info.split()[-1]

        if non_academic_authors:
            records.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": "; ".join(non_academic_authors),
                "Company Affiliation(s)": "; ".join(company_affiliations),
                "Corresponding Author Email": email,
            })

    return pd.DataFrame(records)
