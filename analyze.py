import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from load import *
from process import *


#1 plot data from the accidents, showcasing number of accidents, as well as fatalities
def accident_plot(url):
    df = process_accident_data(url)
    sns.set_theme(style="whitegrid")
    # plots how many accidents occurred in each month, not including the number of fatalities
    df["dates_cleaned"] = pd.to_datetime(df["dates_cleaned"])
    #converts the accident dates into months and removes the dates, groupby groups it by each month. size is the count of accidents
    monthly_count = (df.groupby(df["dates_cleaned"].dt.to_period("M")).size().reset_index(name="count"))
    #turns the dates into months and days on the 1st so that it can be plotted
    monthly_count["dates_cleaned"] = monthly_count["dates_cleaned"].dt.to_timestamp()
    plt.figure(figsize = (18, 8))
    sns.lineplot(data=monthly_count, x="dates_cleaned", y="count")
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    plt.xlabel("Year")
    plt.ylabel("Number of accidents reported")
    plt.title("Accidents Reported per Month")
    plt.tight_layout()
    plt.plot()
    #plots number of fatalities per month
    monthly_fatalities=(df.groupby(df["dates_cleaned"].dt.to_period("M"))["fatalities_cleaned"].sum().reset_index().rename(columns={"dates_cleaned": "month"}))
    monthly_fatalities["month"] = monthly_fatalities["month"].dt.to_timestamp()
    plt.figure(figsize=(18,8))
    sns.lineplot(data=monthly_fatalities, x="month", y="fatalities_cleaned")
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    plt.tight_layout()
    plt.xticks(rotation=90)
    plt.xlabel("Year")
    plt.ylabel("Total Fatalities")
    plt.title("Fatalities per Month")
    plt.tight_layout()
    plt.plot()


#2 timeseries data with corresponding to google search trends on a scale of 0-100
def google_trend_plot(queries_input):
    df = process_google_trend(queries_input)
    df['date'] = pd.to_datetime(df['date'])
    sns.set_theme(style="whitegrid")
    plt.figure(figsize = (16, 10))
    sns.lineplot(data=df, x="date", y="US_average", label = "US Trend Score")
    sns.lineplot(data=df, x="date", y="worldwide_average", label = "International Trend Score")
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    plt.xticks(rotation=45)
    plt.xlabel("Year")
    plt.ylabel("Trend Score")
    plt.title("Google Trend Scores for 'Airplane Accidents' and 'Airplane Crashes'")
    plt.tight_layout()
    plt.legend()
    plt.plot()
    return(df)

#3 graph out passenger enplanements
def enplanements_plot(url):
    df = get_enplanement(url)
    df["year"] = df["period"].dt.year
    # group by totals
    group_year = df.groupby("year")[["Domestic", "International", "Total"]].sum().reset_index()
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(16, 10))
    sns.lineplot(data=group_year, x="year", y="Domestic", label="Domestic Enplanements")
    sns.lineplot(data=group_year, x="year", y="International", label="International Enplanements")
    sns.lineplot(data=group_year, x="year", y="Total", label="Total Enplanements")
    plt.xlabel("Year")
    plt.ylabel("Enplanements")
    plt.title("Domestic, International, and Total Enplanements")
    plt.xticks(group_year["year"], rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

#comparing relevancy of google search trends to the occurrence of accidents
def accident_vs_trends_correlation(accident_url, queries_input):
    accident_df = process_accident_data(accident_url)
    # Convert accident dates to proper monthly periods
    accident_df["period"] = (pd.to_datetime(accident_df["dates_cleaned"]).dt.to_period("M").dt.to_timestamp())
    # Accidents per month
    acc_monthly = (accident_df.groupby("period").size().reset_index(name="accident_count"))
    #uses google trend and obtains data frame
    trend_df = process_google_trend(queries_input)
    # Trend "date" column to datetime using format "Jan 2004"
    trend_df["period"] = pd.to_datetime(trend_df["date"], format="%b %Y")
    # creates a new date frame that lets me merge and create a new df
    trend_monthly = trend_df[["period", "US_average"]].copy()
    merged = pd.merge(acc_monthly, trend_monthly, on="period", how="inner")
    #calcualting correlation value
    correlation_value = merged["accident_count"].corr(merged["US_average"])
    print(f"\nCorrelation between US Trend Score and Monthly Accident Count: {correlation_value:.4f}")
    plt.figure(figsize=(10, 6))
    sns.regplot(data=merged, x="US_average", y="accident_count", scatter_kws={"s": 50}, line_kws={"color": "red"})
    plt.title("Correlation: US Google Trend Score vs Monthly Accident Count")
    plt.xlabel("US Google Trend Score (Average of Crash & Accident Queries)")
    plt.ylabel("Monthly Accident Count")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def fatalities_vs_trends_correlation(accident_url, queries_input):
    accident_df = process_accident_data(accident_url)
    accident_df["fatalities_cleaned"] = pd.to_numeric(accident_df["fatalities_cleaned"], errors="coerce").fillna(0)
    # Convert accident dates to monthly periods
    accident_df["period"] = (pd.to_datetime(accident_df["dates_cleaned"]).dt.to_period("M").dt.to_timestamp())
    # Fatalities per month
    fatality_monthly = (accident_df.groupby("period")["fatalities_cleaned"].sum().reset_index(name="fatality_count"))
    trend_df = process_google_trend(queries_input)
    # Convert time periods so that it can be plotted
    trend_df["period"] = pd.to_datetime(trend_df["date"], format="%b %Y")
    # Keep only US average trend value
    trend_monthly = trend_df[["period", "US_average"]].copy()
    merged = pd.merge(fatality_monthly, trend_monthly, on="period", how="inner")
    correlation_value = merged["fatality_count"].corr(merged["US_average"])
    print(f"\nCorrelation between US Trend Score and Monthly Fatality Count: {correlation_value:.4f}")
    plt.figure(figsize=(10, 6))
    sns.regplot(data=merged, x="US_average", y="fatality_count", scatter_kws={"s": 50}, line_kws={"color": "red"})
    plt.title("Correlation: US Google Trend Score vs Monthly Fatality Count")
    plt.xlabel("US Google Trend Score (Average of Crash & Accident Queries)")
    plt.ylabel("Monthly Fatality Count")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#same thing, but with international trends
def accident_vs_international_trend_correlation(accident_url, queries_input):

    accident_df = process_accident_data(accident_url)
    accident_df["period"] = (pd.to_datetime(accident_df["dates_cleaned"]).dt.to_period("M").dt.to_timestamp())
    acc_monthly = (accident_df.groupby("period").size().reset_index(name="accident_count"))
    trend_df = process_google_trend(queries_input)
    trend_df["period"] = pd.to_datetime(trend_df["date"], format="%b %Y")
    trend_monthly = trend_df[["period", "worldwide_average"]].copy()
    merged = pd.merge(acc_monthly, trend_monthly, on="period", how="inner")
    correlation_value = merged["accident_count"].corr(merged["worldwide_average"])
    print(f"\nCorrelation between International Trend Score and Monthly Accident Count: {correlation_value:.4f}")
    plt.figure(figsize=(10, 6))
    sns.regplot(data=merged, x="worldwide_average", y="accident_count", scatter_kws={"s": 50}, line_kws={"color": "red"})
    plt.title("Correlation: International Trend Score vs Monthly Accident Count")
    plt.xlabel("International Google Trend Score (Worldwide Average)")
    plt.ylabel("Monthly Accident Count")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#fatalities vs international_trend
def fatalities_vs_international_trend_correlation(accident_url, queries_input):
    accident_df = process_accident_data(accident_url)
    accident_df["period"] = (pd.to_datetime(accident_df["dates_cleaned"]).dt.to_period("M").dt.to_timestamp())
    fatalities_monthly = (accident_df.groupby("period")["fatalities_cleaned"].sum().reset_index(name="monthly_fatalities"))
    trend_df = process_google_trend(queries_input)
    trend_df["period"] = pd.to_datetime(trend_df["date"], format="%b %Y")
    trend_monthly = trend_df[["period", "worldwide_average"]].copy()
    merged = pd.merge(fatalities_monthly, trend_monthly, on="period", how="inner")
    correlation_value = merged["monthly_fatalities"].corr(merged["worldwide_average"])
    print(f"\nCorrelation between International Trend Score and Monthly Fatalities: "f"{correlation_value:.4f}")
    plt.figure(figsize=(10, 6))
    sns.regplot(data=merged, x="worldwide_average", y="monthly_fatalities", scatter_kws={"s": 50}, line_kws={"color": "red"})
    plt.title("International Trend Score vs Monthly Fatalities")
    plt.xlabel("International Google Trend Score (Worldwide Average)")
    plt.ylabel("Monthly Fatalities")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def us_trend_vs_enplanements_lag_heatmap(enplanement_url, queries_input, lag_months=0):

    enplanement = get_enplanement(enplanement_url)
    trend = process_google_trend(queries_input)
    #turn dates to datetime
    trend["period"] = pd.to_datetime(trend["date"], format="%b %Y", errors="coerce")
    enplanement["period"] = pd.to_datetime(enplanement["period"], errors="coerce")
    #remove the dates that are not valid
    trend = trend.dropna(subset=["period"])
    enplanement = enplanement.dropna(subset=["period"])
    #using the average US score, copy it over. I'm measuring whether I need to implement lag, according to the argument within my function
    trend_us = trend[["period", "US_average"]].copy()
    if lag_months > 0:
        enp_lagged = enplanement.copy()
        enp_lagged["period"] = enp_lagged["period"] - pd.DateOffset(months=lag_months)
    else:
        enp_lagged = enplanement

    #merge data frames, and then evaluation the correlation
    merged = pd.merge(trend_us, enp_lagged, on="period", how="inner")
    correlation_df = merged[["US_average", "Domestic", "International", "Total"]]
    corr_matrix = correlation_df.corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=0.5, vmin=-1, vmax=1, square=True)
    lag_label = "No Lag"
    if lag_months != 0:
        f"Lag = {lag_months} Months"
    plt.title(f"US Trend vs Enplanements ({lag_label})", fontsize=12)
    plt.tight_layout()
    plt.show()


# this code does the same as above, just using worldwide trends instead
def international_trend_vs_enplanements_lag_heatmap(enplanement_url, queries_input, lag_months=0):

    enplanement = get_enplanement(enplanement_url)
    trend = process_google_trend(queries_input)

    trend["period"] = pd.to_datetime(trend["date"], format="%b %Y", errors="coerce")
    enplanement["period"] = pd.to_datetime(enplanement["period"], errors="coerce")
    trend = trend.dropna(subset=["period"])
    enplanement = enplanement.dropna(subset=["period"])
    trend_intl = trend[["period", "worldwide_average"]].copy()

    if lag_months > 0:
        enp_lagged = enplanement.copy()
        enp_lagged["period"] = enp_lagged["period"] - pd.DateOffset(months=lag_months)
    else:
        enp_lagged = enplanement
    merged = pd.merge(trend_intl, enp_lagged, on="period", how="inner")
    correlation_df = merged[["worldwide_average", "Domestic", "International", "Total"]]
    corr_matrix = correlation_df.corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, linewidths=1, square=True)
    lag_label = "No Lag"
    if lag_months != 0:
        f"Lag = {lag_months} Months"
    plt.title(f"International Trend vs Enplanements ({lag_label})")
    plt.tight_layout()
    plt.show()
