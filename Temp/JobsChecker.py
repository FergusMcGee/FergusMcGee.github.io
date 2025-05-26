import logging
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib
import webbrowser
# Configure logging to output to both file and console
logging.basicConfig(
    level=logging.INFO,  # Log level
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('job_checker.log'),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)


file_name = r"C:\Users\Fergu\source\FergusMcGee.github.io\Data\orglist.csv"

file_path = Path(file_name)

logging.info("Getting file")
# Read the CSV file and ensure it has a 'page_hash' column
df = pd.read_csv(file_path)
if 'page_hash' not in df.columns:
    df['page_hash'] = None  # Add a 'page_hash' column if it doesn't exist

orglist = df.values.tolist()

for index, row in enumerate(orglist):
    url = row[0]
    try:
        # Ensure the URL is valid and starts with http or https
        if not url.startswith(("http://", "https://")):
            logging.warning(f"Skipping invalid URL: {url}")
            continue
        org = url.split('.')[1]

        logging.info(f"Checking {org}")
        
        # Add a User-Agent header to the request
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        page_text = soup.get_text()

        # Create a hash of the page text
        page_hash = hashlib.sha256(page_text.encode('utf-8')).hexdigest()

        # Check if the hash has changed
        changes = False
        if pd.notna(row[1]):  # If a hash already exists
            if row[1] == page_hash:
                logging.info(f"No changes detected for {url}")
            else:
                logging.info(f"Page has changed: {url}")
                changes = True
                webbrowser.open_new_tab(url)
        else:
            logging.info(f"New page detected: {url}")
            changes = True

        if changes:
            # Update the hash in the DataFrame
            df.at[index, 'page_hash'] = page_hash

    except HTTPError as e:
        logging.error(f"HTTP error for URL {url}: {e.code} {e.reason}")
    except URLError as e:
        logging.error(f"Failed to open URL {url}: {e.reason}")
    except Exception as e:
        logging.error(f"An unexpected error occurred for URL {url}: {e}")
if changes:
    # Save the updated DataFrame back to the CSV file
    df.to_csv(file_path, index=False)
    logging.info("Updated CSV file saved.")