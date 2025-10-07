# Favicon Scraper

A Python application that extracts favicons from websites by analyzing HTML meta tags and common favicon locations.

## Features

- **Multiple Detection Methods**: Finds favicons through various methods including:
  - HTML `<link>` tags with `rel="icon"` or `rel="shortcut icon"`
  - Apple touch icons
  - Microsoft tile images
  - Default favicon locations (`/favicon.ico`, `/favicon.png`, etc.)
- **Format Support**: Handles multiple image formats (ICO, PNG, JPG, GIF, SVG)
- **Smart Fallbacks**: Automatically tries common favicon paths if meta tags don't specify one
- **URL Validation**: Ensures the target website is accessible before attempting to scrape
- **Error Handling**: Graceful handling of network timeouts, invalid URLs, and missing favicons
- **CLI Interface**: Easy-to-use command-line interface for batch processing
- **Configurable Options**: Customizable timeout, user agent, and output settings


## Usage

### Command Line Interface

#### Basic Usage
```bash
python favicon_scraper.py <url>
```

#### Save Favicon to File
```bash
python favicon_scraper.py <url> --output favicon.ico
```

#### Batch Processing
```bash
python favicon_scraper.py --batch urls.txt --output-dir favicons/
```

#### Advanced Options
```bash
python favicon_scraper.py <url> \
    --timeout 30 \
    --user-agent "Custom Bot 1.0" \
    --output favicon.ico \
    --verbose
```

### Python API

```python
from favicon_scraper import FaviconScraper

# Initialize scraper
scraper = FaviconScraper(timeout=10, user_agent="MyApp 1.0")

# Get favicon URL
favicon_url = scraper.get_favicon_url("https://example.com")
print(f"Favicon URL: {favicon_url}")

# Download favicon
favicon_data = scraper.download_favicon("https://example.com")
with open("favicon.ico", "wb") as f:
    f.write(favicon_data)

# Get multiple favicons
urls = ["https://google.com", "https://github.com", "https://stackoverflow.com"]
favicons = scraper.get_favicons_batch(urls)
```

## Configuration

### Environment Variables

- `FAVICON_TIMEOUT`: Default timeout in seconds (default: 10)
- `FAVICON_USER_AGENT`: Default user agent string
- `FAVICON_OUTPUT_DIR`: Default output directory for downloaded favicons

### Configuration File

Create a `config.json` file in the project root:

```json
{
    "timeout": 15,
    "user_agent": "FaviconScraper/1.0",
    "output_directory": "./favicons",
    "preferred_formats": ["ico", "png", "svg"],
    "max_file_size": 1048576,
    "follow_redirects": true
}
```

## API Reference

### FaviconScraper Class

#### Methods

- `get_favicon_url(url)`: Returns the favicon URL for a given website
- `download_favicon(url, output_path=None)`: Downloads and saves the favicon
- `get_favicons_batch(urls)`: Processes multiple URLs and returns favicon data
- `validate_url(url)`: Checks if a URL is accessible and returns favicon information

#### Parameters

- `timeout` (int): Request timeout in seconds (default: 10)
- `user_agent` (str): User agent string for HTTP requests
- `follow_redirects` (bool): Whether to follow HTTP redirects (default: True)
- `max_file_size` (int): Maximum favicon file size in bytes (default: 1MB)

## Examples

### Example 1: Single Website
```bash
python favicon_scraper.py https://github.com
# Output: https://github.com/favicon.ico
```

### Example 2: Save to Specific Location
```bash
python favicon_scraper.py https://stackoverflow.com --output so_favicon.ico
# Downloads favicon to so_favicon.ico
```

### Example 3: Batch Processing with CSV
```bash
python favicon_scraper.py --batch websites.csv --output-dir favicons/
```

### Example 4: Python Script
```python
import requests
from favicon_scraper import FaviconScraper

scraper = FaviconScraper()
websites = [
    "https://python.org",
    "https://django.com",
    "https://flask.palletsprojects.com"
]

for site in websites:
    try:
        favicon_url = scraper.get_favicon_url(site)
        print(f"{site}: {favicon_url}")
    except Exception as e:
        print(f"Error getting favicon for {site}: {e}")
```

## Error Handling

The application handles various error scenarios:

- **Network Errors**: Connection timeouts, DNS failures
- **HTTP Errors**: 404, 403, 500 status codes
- **Invalid URLs**: Malformed or unreachable URLs
- **Missing Favicons**: Websites without favicon declarations
- **File System Errors**: Permission issues, disk space

## Performance Considerations

- **Concurrent Requests**: Use batch processing for multiple URLs
- **Caching**: Favicon URLs are cached to avoid redundant requests
- **Rate Limiting**: Built-in delays between requests to be respectful
- **Memory Usage**: Large favicons are streamed to avoid memory issues

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Run with coverage:

```bash
python -m pytest tests/ --cov=favicon_scraper --cov-report=html
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Install pre-commit hooks:
```bash
pre-commit install
```

3. Run linting:
```bash
flake8 favicon_scraper/
black favicon_scraper/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Common Issues

1. **SSL Certificate Errors**
   ```bash
   python favicon_scraper.py --no-verify-ssl <url>
   ```

2. **Permission Denied Errors**
   - Check write permissions for output directory
   - Run with appropriate user permissions

3. **Timeout Issues**
   - Increase timeout value: `--timeout 30`
   - Check network connectivity
   - Verify target website is accessible

4. **No Favicon Found**
   - Some websites don't have favicons
   - Try manual inspection of the website's HTML
   - Check if the site requires JavaScript to load

### Debug Mode

Enable verbose output for debugging:

```bash
python favicon_scraper.py <url> --verbose --debug
```

## Changelog

### Version 1.0.0
- Initial release
- Basic favicon detection and download
- CLI interface
- Python API
- Batch processing support

## Roadmap

- [ ] Web interface for favicon browsing
- [ ] Favicon format conversion (ICO ↔ PNG)
- [ ] Favicon optimization and compression
- [ ] Integration with popular CMS platforms
- [ ] Browser extension for favicon collection
- [ ] Machine learning for favicon quality assessment

## Acknowledgments

- Inspired by the need for reliable favicon extraction
- Built with Python's `requests` and `BeautifulSoup` libraries
- Thanks to the open-source community for inspiration and feedback

## Support

- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/yourusername/favicon-scraper/issues)
- **Discussions**: Join the conversation on [GitHub Discussions](https://github.com/yourusername/favicon-scraper/discussions)
- **Email**: Contact the maintainer at your.email@example.com

---

Made with ❤️ for the web development community
