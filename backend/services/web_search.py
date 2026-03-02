"""
Web search and scraping service for skill learning
"""
from typing import List, Dict, Optional, Any
import requests
from bs4 import BeautifulSoup
from loguru import logger
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config import settings


class WebSearchService:
    """Service for web search and content extraction"""

    def __init__(self):
        self.google_api_key = settings.GOOGLE_SEARCH_API_KEY
        self.google_search_engine_id = settings.GOOGLE_SEARCH_ENGINE_ID
        self.brave_api_key = settings.BRAVE_SEARCH_API_KEY

    async def search(
        self,
        query: str,
        num_results: int = 5,
        search_engine: str = "brave"
    ) -> List[Dict[str, str]]:
        """
        Search the web using available search engines

        Returns:
            List of dicts with keys: title, url, snippet
        """
        if search_engine == "google" and self.google_api_key:
            return await self._google_search(query, num_results)
        elif search_engine == "brave" and self.brave_api_key:
            return await self._brave_search(query, num_results)
        else:
            # Fallback to DuckDuckGo HTML scraping (no API key needed)
            return await self._duckduckgo_search(query, num_results)

    async def _google_search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """Search using Google Custom Search API"""
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": self.google_api_key,
                "cx": self.google_search_engine_id,
                "q": query,
                "num": num_results
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("items", []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                })

            return results

        except Exception as e:
            logger.error(f"Google search error: {str(e)}")
            return []

    async def _brave_search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """Search using Brave Search API"""
        try:
            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {
                "Accept": "application/json",
                "X-Subscription-Token": self.brave_api_key
            }
            params = {
                "q": query,
                "count": num_results
            }

            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("web", {}).get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("description", "")
                })

            return results

        except Exception as e:
            logger.error(f"Brave search error: {str(e)}")
            return []

    async def _duckduckgo_search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """Search using DuckDuckGo HTML scraping (fallback, no API key needed)"""
        try:
            url = "https://html.duckduckgo.com/html/"
            params = {"q": query}
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            response = requests.post(url, data=params, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            results = []

            for result in soup.find_all('div', class_='result')[:num_results]:
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')

                if title_elem:
                    results.append({
                        "title": title_elem.get_text(strip=True),
                        "url": title_elem.get('href', ''),
                        "snippet": snippet_elem.get_text(strip=True) if snippet_elem else ""
                    })

            return results

        except Exception as e:
            logger.error(f"DuckDuckGo search error: {str(e)}")
            return []

    async def scrape_page(self, url: str) -> Dict[str, Any]:
        """
        Scrape content from a webpage

        Returns:
            Dict with keys: title, text, links
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get title
            title = soup.title.string if soup.title else ""

            # Get text content
            text = soup.get_text(separator='\n', strip=True)

            # Get links
            links = []
            for link in soup.find_all('a', href=True):
                links.append({
                    "text": link.get_text(strip=True),
                    "url": link['href']
                })

            return {
                "title": title,
                "text": text[:10000],  # Limit text length
                "links": links[:50],  # Limit number of links
                "url": url
            }

        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return {
                "title": "",
                "text": "",
                "links": [],
                "url": url,
                "error": str(e)
            }

    async def search_and_scrape(
        self,
        query: str,
        num_results: int = 3,
        search_engine: str = "brave"
    ) -> List[Dict[str, Any]]:
        """
        Search for a query and scrape the top results

        Returns:
            List of scraped page data
        """
        search_results = await self.search(query, num_results, search_engine)

        scraped_pages = []
        for result in search_results:
            page_data = await self.scrape_page(result['url'])
            page_data['search_title'] = result['title']
            page_data['search_snippet'] = result['snippet']
            scraped_pages.append(page_data)

        return scraped_pages

    def extract_documentation(self, scraped_data: List[Dict[str, Any]]) -> str:
        """
        Extract and format documentation from scraped pages for LLM consumption
        """
        documentation = ""

        for page in scraped_data:
            documentation += f"\n# {page.get('title', 'Untitled')}\n"
            documentation += f"Source: {page.get('url', '')}\n\n"

            text = page.get('text', '')
            # Clean up the text
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            cleaned_text = '\n'.join(lines)

            # Truncate if too long
            if len(cleaned_text) > 5000:
                cleaned_text = cleaned_text[:5000] + "\n...[truncated]"

            documentation += cleaned_text + "\n\n"
            documentation += "---\n\n"

        return documentation
