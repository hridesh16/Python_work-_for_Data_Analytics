from flask import Flask, render_template, send_from_directory
import os
import pandas as pd

app = Flask(__name__)

# Load the data for trends and analysis
DATA_FILE = "data/analytics_project.db"

def get_data_from_db():
    import sqlite3
    conn = sqlite3.connect(DATA_FILE)
    df = pd.read_sql("SELECT * FROM education_income", conn)
    conn.close()
    return df

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/trends")
def trends():
    # Ensure the visualizations exist
    if not os.path.exists("visualizations/education_income_trends.png"):
        return "Trends visualization not generated yet."

    return render_template("trends.html", trend_image="images/education_income_trends.png")

@app.route("/correlation")
def correlation():
    # Ensure the visualizations exist
    if not os.path.exists("visualizations/growth_correlation.png"):
        return "Correlation heatmap not generated yet."

    return render_template("correlation.html", heatmap_image="images/growth_correlation.png")

# Serve images from the visualizations folder
@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory("visualizations", filename)

if __name__ == "__main__":
    app.run(debug=True)
