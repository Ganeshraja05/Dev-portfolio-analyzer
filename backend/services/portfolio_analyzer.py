import requests
import trafilatura
from bs4 import BeautifulSoup
from newspaper import Article
from fastapi import HTTPException

def fetch_website_content(url: str):
    """Fetch raw website content using requests."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch website: {str(e)}")

def extract_clean_text(url: str):
    """Extract and clean readable text from the given website URL."""
    raw_content = fetch_website_content(url)
    
    # Try Trafilatura first for better text extraction
    extracted_text = trafilatura.extract(raw_content)
    
    if not extracted_text:
        # Fallback: Use BeautifulSoup to extract paragraph text
        soup = BeautifulSoup(raw_content, "lxml")
        extracted_text = " ".join([p.get_text() for p in soup.find_all("p")])

    if not extracted_text:
        raise HTTPException(status_code=400, detail="Unable to extract content from the webpage")

    return extracted_text

def analyze_portfolio(url: str):
    """Analyze the portfolio for metadata and generate a summary."""
    article = Article(url)
    article.download()
    article.parse()
    
    return {
        "title": article.title,
        "authors": article.authors,
        "publish_date": str(article.publish_date),
        "summary": article.text[:500] + "..." if len(article.text) > 500 else article.text
    }
