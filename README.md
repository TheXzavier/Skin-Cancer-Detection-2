# Skin Cancer Detection

## Model Setup

The model file is too large to be included in the repository. To download the model:

1. Upload the model file to a cloud storage service (Google Drive, Dropbox, etc.)
2. Update the URL in `download_model.py` with your storage link
3. Run the download script:

```python
pip install requests tqdm
python download_model.py
```

[Live Site](https://group-g20-skin-cancer-detection.streamlit.app/)

## Running

1. Create a virtual environment

    ```bash
    python3 -m venv venv
    ```

1. Activate the virtual environment

    for Linux and Mac:

    ```bash
    source venv/bin/activate
    ```

    for Windows:

    ```bash
    venv\Scripts\activate
    ```

1. Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

1. Run the app

    ```bash
    streamlit run ./About.py
    ```
