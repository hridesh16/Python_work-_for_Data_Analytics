from flask import Flask, render_template, send_file, request
import pandas as pd
from Apicalls import get_country_education_data, clean_data, save_to_db, plot_trends

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run-analytics", methods=["POST"])
def run_analytics():
    # Parameters for data fetching
    countries = ["US", "CN", "IN", "DE", "JP"]
    indicators = {
        "Primary School Enrollment (% gross)": "SE.PRM.ENRR",
        "Adult Literacy Rate (%)": "SE.ADT.LITR.ZS",
        "GDP per Capita (current US$)": "NY.GDP.PCAP.CD"
    }
    start_year = 2018
    end_year = 2023

    # Fetch, clean, and save data
    data = get_country_education_data(countries, indicators, start_year, end_year)
    data = clean_data(data)
    save_to_db(data)

    # Generate visualizations
    plot_trends(data)

    return render_template("visualization.html", success=True)

@app.route("/view-data")
def view_data():
    # Load data from the database or CSV
    data = pd.read_csv("data/analytics_project.csv")  # Adjust to your data path
    return render_template("visualization.html", tables=[data.to_html(classes='data', header="true")])

@app.route("/view-plot/<filename>")
def view_plot(filename):
    # Return saved plot images
    filepath = f"visualizations/{filename}"
    return send_file(filepath, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
