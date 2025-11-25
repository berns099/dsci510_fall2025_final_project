from load import *
import pandas as pd
import re
from datetime import datetime


#Section to Clean Airplane Accident Data
#1 Function: Cleans up dates: some dates are missing days or even months. This function will instruct it so that
#a date with a missing month will be assigned to the 12th month of the year, or a month with a missing day will still
# be accounted for in the month total by assigning the date to the first day of that month.

def clean_dates(date):
    if date is None:
        return ValueError ('Missing Date')
    new_date = str(date).strip()
    if re.fullmatch(r"\d{4}", new_date): #finds a date column where only the year is given
        return datetime(int(new_date), 12, 1).date()
    month_abbr = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
    month_matching = re.search(month_abbr, new_date)
    year_matching = re.search(r"(\d{4})", new_date)
    day_abbr = r"\b(\d{1,2})(?=\s+"
    day_matching = re.search(day_abbr + month_abbr + ')', new_date) # checking to see if there is a day attached to a month)
    if month_matching and year_matching:
        month_conversion = month_matching.group(1)
        month = datetime.strptime(month_conversion, '%b').month
        year = int(year_matching.group(1))
        if day_matching:
            day = int(day_matching.group(1))
        else:
            day = 1
    elif year_matching: #only year matching, no month or day
        year = int(year_matching.group(1))
        month = 12
        day = 1
    return datetime(year, month, day).date()


#2
#cleans up the data if the fatalities section has a + sign (which is present on the website) and reformats dates using above function
def process_accident_data(url_input:str):
    accident_df = get_accident_table_data(url_input)
    if accident_df is None:
        return ValueError("Error returning data values")
    accident_df["fatalities_cleaned"] = accident_df["fatalities"].apply(lambda x: sum(int(y) for y in re.findall(r"\d+", str(x))))
    accident_df["dates_cleaned"] = accident_df["accident_date"].apply(clean_dates)
    return accident_df


#use dataframe pulled from the api and create new columns
def process_google_trend(queries_input):
    trend_df = get_trend_data(queries_input)
    #replaces the blanks with the overall world search results
    trend_df["geo"] = trend_df["geo"].replace({"": "world"})
    trend_df["date"] = pd.to_datetime(trend_df["date"])
    #searches for either airplane crash or airplane accident
    pattern = re.compile(r"(airplane crash|airplane accident)")
    trend_results = {}

    for i, row in trend_df.iterrows():
        if not pattern.search(row["query"]):
            continue
        query_clean = pattern.search(row["query"]).group(1).replace(" ", "_")
        geo = "US" if row["geo"] == "US" else "world"
        date = row["date"]
        value = row["value"]
        if date not in trend_results:
            trend_results[date] = {
                "airplane_crash_US": None,
                "airplane_crash_world": None,
                "airplane_accident_US": None,
                "airplane_accident_world": None,
            }

        col_name = f"{query_clean}_{geo}"
        trend_results[date][col_name] = value

    df = pd.DataFrame.from_dict(trend_results, orient="index")
    df = df.reset_index().rename(columns={"index": "date"})

    df["US_average"] = df[["airplane_crash_US", "airplane_accident_US"]].mean(axis=1)
    df["worldwide_average"] = df[["airplane_crash_world", "airplane_accident_world"]].mean(axis=1)

    df["period_month"] = df["date"].dt.to_period("M").dt.to_timestamp()

    return df


