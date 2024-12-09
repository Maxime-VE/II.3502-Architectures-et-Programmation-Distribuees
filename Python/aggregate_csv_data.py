import pandas as pd
import os

# Import the data (.csv file) as a Pandas dataframe
input_file = r"..\Results\covid_analysis_results1.csv"
df_covid = pd.read_csv(input_file)

# Set a new column to check if location is a country (depending on the continent field emptyness)
df_covid['is_country'] = ~df_covid['continent'].isna()
df_countries_only = df_covid[df_covid['is_country']]

# Aggregation by continent
continent_aggregates = df_countries_only.groupby(['continent', 'date']).agg({'total_cases': 'mean', 'total_deaths': 'mean'}).reset_index()

#Aggregation by country
country_aggregates = df_countries_only.groupby('location').agg({'total_cases': 'max', 'total_deaths': 'max', 'people_fully_vaccinated': 'max', 'vaccinated_percentage': 'max', 'population': 'first'}).reset_index()

# Top 10 vaccinated country rate
top_vaccinated_countries = country_aggregates.nlargest(10, 'vaccinated_percentage')

#Save data to a .csv file
output_folder = r"..\Results"
output_file_continent = os.path.join(output_folder, "continent_daily_averages.csv")
continent_aggregates.to_csv(output_file_continent, index=False)
output_file_country = os.path.join(output_folder, "country_totals_stats.csv")
country_aggregates.to_csv(output_file_country, index=False)
output_file_top_vaccinated = os.path.join(output_folder, "top_10_vaccinated_countries.csv")
top_vaccinated_countries.to_csv(output_file_top_vaccinated, index=False)

print(f"Fichiers générés :\n - {output_file_continent}\n - {output_file_country}\n - {output_file_top_vaccinated}")
