import os
import pandas as pd

# Import the data (.csv file) as a Pandas dataframe
df_covid = pd.read_csv(r"..\Data\owid-covid-data.csv")

# Keep only the desired column
columns_list = ["continent", "location", "date", "total_cases", "total_deaths", "population", "people_fully_vaccinated"]
df_covid_parsed = df_covid[columns_list].copy()

# Display the number of NAN values in each column
# print(df_covid_parsed.isnull().sum())

# Convert the date column to datetime
df_covid_parsed['date'] = pd.to_datetime(df_covid_parsed['date'])

# Sort data by location and date
df_covid_parsed = df_covid_parsed.sort_values(by=["location", "date"])

#  Fill the missing values
columns_to_fill = ["total_cases", "total_deaths", "people_fully_vaccinated"]
for column in columns_to_fill:
    df_covid_parsed[column] = (df_covid_parsed.groupby("location")[column].transform(lambda group: group.ffill().bfill()))

# Compute vaccination percentage
df_covid_parsed['vaccinated_percentage'] = (df_covid_parsed['people_fully_vaccinated'] / df_covid_parsed['population']) * 100

# Set maximum percentage of vaccination to 100% (since we fill missing value with interpolation methods and result may overflow)
df_covid_parsed['vaccinated_percentage'] = df_covid_parsed['vaccinated_percentage'].clip(upper=100)

# Set display format for floats
pd.options.display.float_format = '{:.2f}'.format

# Save data to a .csv file
output_file = r"..\Results\covid_analysis_results1.csv"
os.makedirs(os.path.dirname(output_file), exist_ok=True)
df_covid_parsed.to_csv(output_file, index=False)

print(f"Les résultats ont été sauvegardés dans le fichier : {output_file}")
