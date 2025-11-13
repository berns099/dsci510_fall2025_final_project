from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
import json

url = 'https://aviation-safety.net/database/year/2004/1'
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}
content = requests.get(url, headers=headers)
soup = BeautifulSoup(content.text, 'html.parser')
content_tables = soup.find('table', {"class": "hp"})
rows = content_tables.find_all('tr')
accident_dict = []
current_accident = None
modified_date = None
for row in rows:
    cells = row.find_all('td')
    raw_data = cells[0].text.strip()
    if re.match(r"^[A-Za-z]",raw_data):
        if re.search(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b", raw_data): # checks to see if a month is included
            modified_date = (re.search(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b", raw_data) +
                             " " + re.search(r"\b\d{4}\b",raw_data))
        else: #checks to see if a year is included
            modified_date = re.search(r"\b\d{4}\b", raw_data)
    modified_date = re.search()

    if re.search(r"\+", cells[4].text.strip()): #checks to see if there is a + condition
        text=cells[4].text.strip()
        parts = text.split('+')
        modified_fatality = sum(parts)
    else:
        modified_fatality = cells[4].text.strip()

    if re.search("", cells[5].text.strip()):
        text=cells[5].text.strip()
    current_accident = {"accident date": modified_date,
                       "fatalities": modified_fatality,
                       "country": cells[1].text.rstrip()}
    else:
        continue
    rocket_dict.append(current_rocket)
output_file = "space_launches.json"
with open(output_file, 'w') as json_file:
    json.dump(rocket_dict, json_file)
