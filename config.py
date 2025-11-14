from pathlib import Path
from dotenv import load_dotenv

# project configuration from .env (secret part)
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)  # loads into os.environ

# project configuration
DATA_DIR = "../data"
RESULTS_DIR = "../results"

# data sources configuration
ENPLANEMENTS_CSV = 'https://docs.google.com/spreadsheets/d/1Zxxlbj3-jXBdDsURy_9wI5mkQD-o8g3IH3eDGBs6dgQ/export?format=csv'
SEARCH_QUERIES = 'airplane accident,airplane crash'
AVIATION_ACCIDENTS = 'https://aviation-safety.net/database/year'

