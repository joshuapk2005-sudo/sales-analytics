from __future__ import annotations

from pathlib import Path
import urllib.request

REMOTE_DATA_URL = "https://raw.githubusercontent.com/gustika17/healthcare-dataset-stroke-data.csv/main/healthcare-dataset-stroke-data.csv"
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "healthcare-dataset-stroke-data.csv"


def download_dataset() -> Path:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(REMOTE_DATA_URL, DATA_PATH)
    return DATA_PATH


if __name__ == "__main__":
    file_path = download_dataset()
    print(f"Downloaded dataset to: {file_path}")
