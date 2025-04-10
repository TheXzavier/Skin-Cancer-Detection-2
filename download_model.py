import os
import requests
from tqdm import tqdm
import re

def download_file_from_google_drive(file_id, destination):
    """
    Download a file from Google Drive using its file ID
    """
    if os.path.exists(destination):
        print(f"Model file already exists at {destination}")
        return
    
    print(f"Downloading model file to {destination}...")
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    # Google Drive API URL
    URL = "https://docs.google.com/uc?export=download"
    
    # Start session to handle cookies
    session = requests.Session()
    
    # Make initial request
    response = session.get(URL, params={'id': file_id}, stream=True)
    
    # Check if the file is large and requires confirmation
    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
            break
    
    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    
    # Get file size if available
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    
    with open(destination, 'wb') as file, tqdm(
            desc=os.path.basename(destination),
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
        for data in response.iter_content(block_size):
            size = file.write(data)
            bar.update(size)
    
    print("Download complete!")

def extract_file_id(drive_link):
    """
    Extract the file ID from a Google Drive sharing link
    """
    pattern = r"/d/([a-zA-Z0-9_-]+)"
    match = re.search(pattern, drive_link)
    if match:
        return match.group(1)
    return None

if __name__ == "__main__":
    # Your Google Drive sharing link
    drive_link = "https://drive.google.com/file/d/1d_zmXyypxBe7h5rh07IXgjxgpwMRzeyu/view?usp=sharing"
    
    # Extract file ID from the link
    file_id = extract_file_id(drive_link)
    if not file_id:
        print("Invalid Google Drive link. Please check the URL.")
        exit(1)
    
    model_path = os.path.join("model", "model.h5")
    
    download_file_from_google_drive(file_id, model_path)