from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
from src.utils import validate_url

def parse_sizes_attribute(sizes):
    """Parse the 'sizes' attribute to get the largest dimension."""
    if not sizes:
        return 0
    try:
        # Handle formats like '180x180' or '192x192'
        dimensions = sizes.split('x')
        return int(dimensions[0]) if dimensions else 0
    except (ValueError, IndexError):
        return 0

def get_favicon_urls(url):
    """Fetch all favicon URLs from the website with their sizes."""
    if not validate_url(url):
        raise ValueError("Invalid URL")

    try:
        # Send a GET request to the website
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all favicon-related link tags
        favicon_tags = soup.find_all('link', rel=['icon', 'shortcut icon', 'apple-touch-icon'])

        # Collect all favicon URLs and their sizes
        favicon_urls = []
        for tag in favicon_tags:
            href = tag.get('href')
            if href:
                sizes = tag.get('sizes', '')
                size_value = parse_sizes_attribute(sizes)
                # Assign default size for apple-touch-icon (typically larger)
                if 'apple-touch-icon' in tag.get('rel', []):
                    size_value = max(size_value, 180)  # Assume 180x180 if no sizes
                favicon_urls.append((urljoin(url, href), size_value))

        # Fallback: Check for default /favicon.ico
        parsed_url = urlparse(url)
        default_favicon = f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"
        response = requests.head(default_favicon, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            favicon_urls.append((default_favicon, 32))  # Assume 32x32 for default favicon.ico

        if not favicon_urls:
            print("No favicons found")
            return []

        # Log found favicons
        print("Found favicons:")
        for url, size in favicon_urls:
            print(f" - {url} (size: {size}px)")
        return favicon_urls
    except requests.RequestException as e:
        print(f"Error fetching favicon URLs: {e}")
        return []