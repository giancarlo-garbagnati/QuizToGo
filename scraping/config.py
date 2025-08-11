import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    base_url: str = os.getenv("BASE_URL", "")
    username: str = os.getenv("USERNAME", "")
    password: str = os.getenv("PASSWORD", "")
    headless: bool = os.getenv("HEADLESS", "1") == "1"
    storage_state: str = os.getenv("STORAGE_STATE", "scraping/storage_state.json")
