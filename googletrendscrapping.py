from serpapi import GoogleSearch
import time
import json
from dotenv import load_dotenv
import pandas as pd
import os

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
    # with open("google_trends_airplane.json", "w") as f:
    #     json.dump(all_results, f, indent=2)
    df = pd.DataFrame(all_results)