import os
import pandas as pd

data_dict = {}

# Import the data (.csv file) as a Pandas dataframe
df_covid = pd.read_csv(r"owid-covid-data.csv")

# Parse the desired column in file
df_covid_parsed = df_covid[["location", "date", "total_cases","total_deaths","population","people_fully_vaccinated" ]]


for column in df_covid_parsed:
    data_dict[column] = {
        "has_nan":df_covid_parsed[column].isnull().values.any(),
        "number_nan":df_covid_parsed[column].isnull().sum().sum()
        }


for element in data_dict:
    if data_dict[element]["has_nan"]:
        df_covid_parsed[element] = df_covid_parsed.groupby("location")[element].transform(
            lambda x: x.fillna(x.mean())
        )

#Utils

#Get Nan values for each column
print(df_covid_parsed.isnull().sum())


df_covid_parsed['vaccinated_percentage'] = (df_covid_parsed['people_fully_vaccinated'] / df_covid_parsed['population']) * 100

pd.options.display.float_format = '{:.2f}'.format
print(df_covid_parsed[['location', 'people_fully_vaccinated', 'population','vaccinated_percentage']].groupby(by='location').last())
