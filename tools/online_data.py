import json
import requests # New import for web fetching
from bs4 import BeautifulSoup # New import for HTML parsing

def get_wikipedia_data(query: str) -> str:
    """
    Fetches the full main content of a Wikipedia article based on a query.
    
    Args:
        query (str): The chemical or scientific topic to retrieve from Wikipedia.
        
    Returns:
        str: A JSON string containing the article title, full text, and page metadata.
    """
    search_url = f"https://en.wikipedia.org/wiki/{requests.utils.quote(query)}"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        page_title = soup.find("h1", id="firstHeading").text.strip()

        # Extract the main content
        content_div = soup.find("div", class_="mw-parser-output")
        paragraphs = content_div.find_all(['p', 'h2', 'h3', 'ul', 'ol'])  # Main content only

        article_text = ""
        for tag in paragraphs:
            if tag.name in ["h2", "h3"]:
                section_title = tag.get_text(strip=True).replace("[edit]", "")
                article_text += f"\n\n### {section_title}\n\n"
            else:
                text = tag.get_text(strip=True)
                if text:
                    article_text += f"{text}\n\n"

        if article_text.strip():
            return json.dumps({
                "status": "success",
                "query": query,
                "wikipedia_url": search_url,
                "title": page_title,
                "article_text": article_text.strip()
            })
        else:
            return json.dumps({
                "status": "error",
                "query": query,
                "wikipedia_url": search_url,
                "message": "No article text found on the page."
            })

    except requests.exceptions.RequestException as e:
        return json.dumps({
            "status": "error",
            "query": query,
            "wikipedia_url": search_url,
            "message": f"Network error: {str(e)}"
        })
    except Exception as e:
        return json.dumps({
            "status": "error",
            "query": query,
            "wikipedia_url": search_url,
            "message": f"Parsing error: {str(e)}"
        })

