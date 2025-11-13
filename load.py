from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from serpapi import GoogleSearch
import time
from dotenv import load_dotenv
import os
import gdown


# --- 1. DOWNLOAD ACCIDENT DATA FROM AVIATION SAFETY NETWORK
# --- OUTPUTS CSV FILE
def get_accident_table_data(url_input):
    accident_dict = []
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }
    year = 2004
    while year <2026:
        i = 1
        while True:
            url = f'{url_input}/{year}/{i}'
            try:
                content = requests.get(url, headers=headers)
            except:
                raise ValueError("")
            soup = BeautifulSoup(content.text, 'html.parser')
            content_tables = soup.find('table', {"class": "hp"})
            if content_tables is None:
                break
            rows = content_tables.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) < 5:
                    continue

                flag_img = cells[6].find('img')
                marker = "International"
                if flag_img:
                    flag = flag_img.get('src')
                    if re.search(r"/N\.gif", flag):
                        marker = "Domestic"

                current_accident = {"accident_date": cells[0].find('a').get_text().strip(),
                                    "operator": cells[3].text.strip(),
                                   "fatalities": cells[4].text.strip(),
                                   "marker": marker}
                accident_dict.append(current_accident)
            i += 1
        year += 1
    df = pd.DataFrame(accident_dict)
    print(df.head())

    #
    # output_file = "accidents.csv"
    # with open(output_file, mode="w", newline="", encoding="utf-8") as csv_file:
    #     fieldnames = ["accident_date", "operator", "fatalities", "marker"]
    #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #     writer.writeheader()
    #     writer.writerows(accident_dict)
    # print(f"{len(accident_dict)} records saved to {output_file}")

# --- 2. USE SERPAPI to determine

def get_trend_data(queries_input):
    load_dotenv()
    API_KEY = os.getenv("SERPAPI_KEY")
    queries = queries_input.split(",")
    location = ["", "US"]
    all_results = []
    i = 0
    while i < 2:
        for query in queries:
            params = {
                "engine": "google_trends",
                "q": query,
                "data_type": "TIMESERIES",
                "date": "all",
                "api_key": API_KEY,
                "geo" : location[i]
            }

            search = GoogleSearch(params)
            results = search.get_dict()

            # Extract the "interest_over_time" data if available
            interest_data = results.get("interest_over_time", {}).get("timeline_data", [])
            for entry in interest_data:
                all_results.append({
                    "query": query,
                    "date": entry.get("date"),
                    "value": entry.get("values")[0].get("extracted_value"),
                    "geo": location[i]
                })
            time.sleep(2)
        i+=1
    df = pd.DataFrame(all_results)
    print(df.head())


#3 TRANSTATS - Track passenger enplanements

def get_enplanement(url):
   print(f"--- Loading data from Web URL: {url[:50]}... ---")

   try:
       gdown.download(url,"enplanements.csv", quiet=False)
       df = pd.read_csv("enplanements.csv")
       print("Web CSV data loaded successfully.")
       print(df.head())
       return df
   except Exception as e:
       print(f"Error loading data from URL: {e}")
       return None