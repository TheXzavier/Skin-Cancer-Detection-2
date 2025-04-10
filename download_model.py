import os
import requests
import re

def download_file_from_google_drive(file_id, destination):
    """
    Download a file from Google Drive using its file ID
    """
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    URL = "https://docs.google.com/uc?export=download"
    
    session = requests.Session()
    
    # First request to get the confirmation token
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)
    
    if token:
        params = {'id': file_id, 'confirm': token}
    else:
        params = {'id': file_id}
        
    # Add special headers to mimic browser behavior
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Second request with confirmation token
    response = session.get(URL, params=params, headers=headers, stream=True)
    
    # Create progress bar
    progress_bar = st.progress(0)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 32768  # 32 KB
    written = 0
    
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, 'wb') as f:
        for data in response.iter_content(block_size):
            written += len(data)
            f.write(data)
            if total_size:
                progress = min(written / total_size, 1.0)
                progress_bar.progress(progress)
    
    progress_bar.empty()
    return destination

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