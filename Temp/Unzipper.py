

# 

from pathlib import Path
import zipfile
import shutil

def extract_and_cleanup(source_folder, target_folder):
    # Convert input paths to Pathlib objects
    source_path = Path(source_folder)
    target_path = Path(target_folder)
    
    # Ensure the target folder exists
    target_path.mkdir(parents=True, exist_ok=True)
    
    # Iterate through all zip files in the source folder
    for zip_file in source_path.glob("*.zip"):
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(target_path)
                print(f"Extracted: {zip_file}")
        except zipfile.BadZipFile:
            print(f"Bad ZIP file: {zip_file}")
    
    # Remove any non-JPG files from the target folder
    for file in target_path.iterdir():
        if not file.is_file() or file.suffix.lower() != '.jpg':
            try:
                if file.is_dir():
                    shutil.rmtree(file)  # Delete directories
                else:
                    file.unlink()  # Delete files
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting {file}: {e}")

# Example usage
source_folder = r"C:\Downloads\www.southern-charms4.com"
target_folder = r"C:\Temp\S_Charms"
extract_and_cleanup(source_folder, target_folder)
