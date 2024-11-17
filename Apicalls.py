import requests
import pandas as pd
import os

# Fetch indicator data using World Bank API
def fetch_indicator_data(country, indicator, start_year, end_year):
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
    params = {"format": "json", "date": f"{start_year}:{end_year}"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 1:
            return [
                {
                    "country": country,
                    "indicator": indicator,
                    "year": int(entry["date"]),
                    "value": entry.get("value")
                }
                for entry in data[1]
            ]
    return []

# Fetch data for multiple indicators and countries
def get_country_data(countries, indicators, start_year, end_year):
    all_data = []
    for country in countries:
        for name, code in indicators.items():
            print(f"Fetching data for {country} - {name}")
            indicator_data = fetch_indicator_data(country, code, start_year, end_year)
            for entry in indicator_data:
                entry["indicator_name"] = name
                all_data.append(entry)
    return pd.DataFrame(all_data)
  # Clean and process data
def clean_data(df):
    df.dropna(subset=["value"], inplace=True)
    df["value"] = df["value"].astype(float)
    return df

# Calculate growth rate
def calculate_growth(df):
    df["growth"] = df.groupby(["country", "indicator_name"])["value"].pct_change() * 100
    return df
import sqlite3

# Save to SQLite database
def save_to_db(df, db_name="data/analytics_project.db", table_name="education_income"):
    os.makedirs("data", exist_ok=True)
    with sqlite3.connect(db_name) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Data saved to database: {db_name}, table: {table_name}")

# Load data from database
def load_from_db(db_name="data/analytics_project.db", table_name="education_income"):
    with sqlite3.connect(db_name) as conn:
        return pd.read_sql(f"SELECT * FROM {table_name}", conn)
import matplotlib.pyplot as plt
import seaborn as sns

# Compare education and income trends
def plot_trends(df):
    os.makedirs("visualizations", exist_ok=True)

    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df, x="year", y="value", hue="indicator_name", style="country", markers=True)
    plt.title("Education and Income Trends (Last 5 Years)")
    plt.xlabel("Year")
    plt.ylabel("Value")
    plt.legend(title="Indicator")
    plt.tight_layout()
    plt.savefig("visualizations/education_income_trends.png")
    plt.show()

# Heatmap for growth correlation
def plot_correlation(df):
    pivot_data = df.pivot_table(values="growth", index="country", columns="indicator_name", aggfunc="mean")
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_data, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Growth Correlation Between Education and Income")
    plt.tight_layout()
    plt.savefig("visualizations/growth_correlation.png")
    plt.show()

