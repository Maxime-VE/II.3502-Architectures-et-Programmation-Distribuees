from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, avg, max, first, lit, expr
from pyspark.sql.window import Window
from pyspark.sql.functions import last

# Init Spark
spark = SparkSession.builder.appName("COVID Analysis").getOrCreate()

# Paths
input_file = "../Data/owid-covid-data.csv"
output_folder = "../SparkOutput"

# Load data input
df_covid = spark.read.csv(input_file, header=True, inferSchema=True)

# Keep only the desired column
columns_list = ["continent", "location", "date", "total_cases", "total_deaths", "population", "people_fully_vaccinated"]
df_covid = df_covid.select(columns_list)

df_covid = df_covid.withColumn("date", col("date").cast("date"))
window_spec = Window.partitionBy("location").orderBy("date")

for col_name in ["total_cases", "total_deaths", "people_fully_vaccinated"]:
    df_covid = df_covid.withColumn(col_name, last(col_name, ignorenulls=True).over(window_spec))

# Vaccination rate
df_covid = df_covid.withColumn( "vaccinated_percentage", (col("people_fully_vaccinated") / col("population") * 100).cast("double")).withColumn("vaccinated_percentage", when(col("vaccinated_percentage") > 100, 100).otherwise(col("vaccinated_percentage")))

df_covid = df_covid.withColumn("is_country", when(col("continent").isNotNull(), lit(True)).otherwise(lit(False)))
df_countries_only = df_covid.filter(col("is_country") == True)

# Aggregation by continent
continent_aggregates = df_countries_only.groupBy("continent", "date").agg(avg("total_cases").alias("avg_total_cases"), avg("total_deaths").alias("avg_total_deaths"))

# Aggregation by countries
country_aggregates = df_countries_only.groupBy("location").agg(
    max("total_cases").alias("total_cases"),
    max("total_deaths").alias("total_deaths"),
    max("people_fully_vaccinated").alias("people_fully_vaccinated"),
    max("vaccinated_percentage").alias("vaccinated_percentage"),
    first("population").alias("population")
)

# Top 10 vaccination rate by countries
top_vaccinated_countries = country_aggregates.orderBy(col("vaccinated_percentage").desc()).limit(10)

# Save as .csv file
continent_aggregates.coalesce(1).write.csv(f"{output_folder}/continent_daily_averages.csv", header=True, mode="overwrite")
country_aggregates.write.csv(f"{output_folder}/country_totals_stats.csv", header=True, mode="overwrite")
top_vaccinated_countries.write.csv(f"{output_folder}/top_10_vaccinated_countries.csv", header=True, mode="overwrite")

print(f"File added to : {output_folder}")

# Stopper Spark
spark.stop()
