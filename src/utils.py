from urllib.parse import urlparse

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def get_file_extension(content_type):
    return '.ico' if 'image/x-icon' in content_type else '.png'