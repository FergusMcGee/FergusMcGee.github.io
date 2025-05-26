import requests
from pathlib import Path
from tqdm import tqdm


home_dir = Path.home()
file_path = home_dir.joinpath("OneDrive2","OneDrive","Temp","VhiLinks.txt")
# Read the URLs from the file
with open(file_path, 'r') as file:
    urls = file.readlines()

# Strip any extra whitespace like newlines
urls = [url.strip() for url in urls]

# Set up authentication headers or cookies
headers = {
    "Authorization": "Bearer YOUR_TOKEN",  # Or use cookies={'session': 'abc123'} if session-based
    # "User-Agent": "Mozilla/5.0",  # Optional, sometimes needed
}
cookies = {
    'JSESSIONIDWC': 'e8sNJUK4cKIutvapsLgm4heT84aA8qJPZafiLC-dLRWWd11pLZI8!486573450',
    'JSESSIONID': 'WksNRDtc7vAgKmhDRCcAff-NH3hnIuYsAQRlhNQ-Seced4b_ScPF!486573450',
    'cookiesession1': '678ADA59319DCE87231EA279B0241147',
    'accessToken': 'eyJraWQiOiJCUjBuYzNqMmRSMU1QdWNTdjZNUm12OFVhNHVGT2NjOUM0YmhjMklORnE0IiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULmxGS2tGbnBpZFpmQ3dxX3ZCb1ZfN2tITjVIdk5XSGJSbUlNUDhCQVJCaFkiLCJpc3MiOiJodHRwczovL2FkbWluLWRpZ2l0YWwudmhpLmllL29hdXRoMi9hdXM4eGRsc2YwZmdqYzFSMDQxNyIsImF1ZCI6ImFwaTovL015VkhJIiwiaWF0IjoxNzQ4Mjc0MjY0LCJleHAiOjE3NDgyNzUxNjQsImNpZCI6IjBvYTh4ZG5vODgzT1ZSbmhlNDE3IiwidWlkIjoiMDB1OTEwOXN3N2Z6UTk1N3g0MTciLCJzY3AiOlsiZW1haWwiLCJwcm9maWxlIiwib3BlbmlkIiwiTXlWSEkucHJvZmlsZSJdLCJhdXRoX3RpbWUiOjE3NDgyNzQyNjIsInN1YiI6ImZlcmd1c21jZ2VlQGdtYWlsLmNvbSIsInJvbGVzIjpbIk15VkhJIl0sInBhcnRuZXJJRCI6IjM4MzAyOTIifQ.NGR9ullosgFl5IpUur4j0cqtP8iWEilXby-OpHXBhRfWYO60SyAfFUjMbTnalBuY49H9AeKifrTZrAwR7lKT3BUYmrCiE_ODj-yjLuxxb3nsnemDePUolo8unzUbW3mnUPhfSuA2dYpZx0V31FzetUU5rFFoExFHXOmxXhjeRzphLZQtSGN0eFkBPc-6Z-E8MM4SVVlJkUG4AA_6x7iV46dPgOYumBa3Z_1J0Jx_4WN7ORiq_nmW5PSsjeL62gR9CtIPxnuIMIOUyt-Mg0Ao-98asyZgWPTSZa0mxphiXUtDOEvvABz5KRaWNO4HUVMITNmgmrCCj62j_hKgKknAQQ'
}

output_dir = Path("downloads")
output_dir.mkdir(exist_ok=True)

# Download the PDFs
for url in tqdm(urls, desc="Downloading PDFs"):
    try:
        response = requests.get(url, cookies=cookies, headers=headers, allow_redirects=True)

        if "application/pdf" in response.headers.get("Content-Type", ""):
            # Derive a filename (fallback if none)
            filename = url.split("/")[-1] + ".pdf"
            filepath = output_dir / filename
            with open(filepath, "wb") as f:
                f.write(response.content)
        else:
            print(f"[WARN] Not a PDF at {url} — content type was: {response.headers.get('Content-Type')}")

    except Exception as e:
        print(f"[ERROR] Failed to download {url}: {e}")