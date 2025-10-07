import requests
import os
from pathlib import Path
import platform
from src.utils import get_file_extension

try:
    # Windows-specific import
    from win32com.shell import shell, shellcon
except ImportError:
    shell = None  # Will handle non-Windows systems

def get_downloads_folder():
    """Get the user's Downloads folder path for macOS and Windows, with fallback."""
    try:
        if platform.system() == "Windows" and shell is not None:
            downloads_path = Path(shell.SHGetKnownFolderPath(shellcon.FOLDERID_Downloads, 0, 0))
        else:
            downloads_path = Path.home() / "Downloads"
        
        if downloads_path.exists() and downloads_path.is_dir():
            if os.access(downloads_path, os.W_OK):
                print(f"Using Downloads folder: {downloads_path}")
                return downloads_path
            else:
                print(f"Downloads folder ({downloads_path}) is not writable")
        else:
            print(f"Downloads folder ({downloads_path}) does not exist")
    except Exception as e:
        print(f"Error accessing Downloads folder: {e}")
    
    fallback_path = Path.cwd()
    print(f"Falling back to current directory: {fallback_path}")
    return fallback_path

def download_all_favicons(favicon_urls, output_name="favicon"):
    """Download all favicon URLs to the Downloads folder."""
    downloads_path = get_downloads_folder()
    
    for favicon_url, size in favicon_urls:
        try:
            # Fetch the favicon
            response = requests.get(favicon_url, timeout=10)
            response.raise_for_status()
            
            # Determine file extension from content type
            extension = get_file_extension(response.headers.get('content-type', ''))
            
            # Use size in filename if available, otherwise use generic name
            if size > 0:
                base_name = f"{output_name}_{size}x{size}"
            else:
                base_name = output_name
            
            output_file = downloads_path / f"{base_name}{extension}"
            
            # Ensure unique filename to avoid overwriting
            counter = 1
            while output_file.exists():
                output_file = downloads_path / f"{base_name}_{counter}{extension}"
                counter += 1
            
            # Save the favicon
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"Favicon downloaded to: {output_file}")
        except requests.RequestException as e:
            print(f"Error downloading favicon {favicon_url}: {e}")
        except OSError as e:
            print(f"Error saving favicon to {output_file}: {e}")