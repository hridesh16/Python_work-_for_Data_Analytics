from Apicalls import*

if __name__ == "__main__":
    # Define parameters
    countries = ["US", "CN", "IN", "DE", "JP"]
    start_year = 2018
    end_year = 2023
    indicators = {
        "Primary School Enrollment (% gross)": "SE.PRM.ENRR",
        "Adult Literacy Rate (%)": "SE.ADT.LITR.ZS",
        "GDP per Capita (current US$)": "NY.GDP.PCAP.CD"
    }

    # Fetch, process, and save data
    data = get_country_data(countries, indicators, start_year, end_year)
    data = clean_data(data)
    data = calculate_growth(data)
    save_to_db(data)

    # Load data and visualize
    data = load_from_db()
    plot_trends(data)
    plot_correlation(data)
