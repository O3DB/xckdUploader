import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    'VK_TOKEN': os.getenv('VK_TOKEN'),
    'GROUP_ID': os.getenv('GROUP_ID'),
}
