from src.scraper import get_favicon_urls
from src.downloader import download_all_favicons

def main():
    website = input("Enter the website URL (e.g., https://example.com): ")
    favicon_urls = get_favicon_urls(website)
    if favicon_urls:
        download_all_favicons(favicon_urls)
    else:
        print("No favicons found for the website.")

if __name__ == "__main__":
    main()