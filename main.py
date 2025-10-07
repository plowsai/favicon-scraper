import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

def get_favicon_url(url):
    try:
        # Send a GET request to the website
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for favicon in common link tags
        favicon_tags = [
            soup.find('link', rel='icon'),
            soup.find('link', rel='shortcut icon'),
            soup.find('link', rel='apple-touch-icon')
        ]
        
        # Filter out None values and get the first valid favicon URL
        for tag in favicon_tags:
            if tag and tag.get('href'):
                favicon_url = tag['href']
                # Convert relative URL to absolute URL
                favicon_url = urljoin(url, favicon_url)
                return favicon_url
        
        # Fallback: try common favicon location
        parsed_url = urlparse(url)
        default_favicon = f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"
        response = requests.head(default_favicon, timeout=5)
        if response.status_code == 200:
            return default_favicon
        
        return None
    except requests.RequestException as e:
        print(f"Error fetching favicon URL: {e}")
        return None

def download_favicon(favicon_url, output_path="favicon"):
    try:
        # Fetch the favicon
        response = requests.get(favicon_url, timeout=10)
        response.raise_for_status()
        
        # Determine file extension from URL or content type
        content_type = response.headers.get('content-type', '')
        extension = '.ico' if 'image/x-icon' in content_type else '.png'
        output_file = f"{output_path}{extension}"
        
        # Save the favicon
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"Favicon downloaded to {output_file}")
    except requests.RequestException as e:
        print(f"Error downloading favicon: {e}")
    except OSError as e:
        print(f"Error saving favicon: {e}")

def scrape_favicon(website_url, output_path="favicon"):
    favicon_url = get_favicon_url(website_url)
    if favicon_url:
        print(f"Favicon found: {favicon_url}")
        download_favicon(favicon_url, output_path)
    else:
        print("No favicon found for the website.")

if __name__ == "__main__":
    # Example usage
    website = input("Enter the website URL (e.g., https://example.com): ")
    scrape_favicon(website)