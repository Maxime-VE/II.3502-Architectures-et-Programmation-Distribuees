import sys
from itertools import count

from pyspark import SparkContext, SparkConf

if __name__ == "__main__":
    # Configuration de l'application Spark
    conf = SparkConf().setAppName("Spark Count")
    sc = SparkContext(conf=conf)

    inputFile = sys.argv[1]
    textFile = sc.textFile(inputFile)

    wordCounts = (
        textFile
        .flatMap(lambda line: line.split())
        .map(lambda word: (word, 1))
        .reduceByKey(lambda a, b: a + b)
    )

    output = wordCounts.collect()
    nbr_word=0
    for word, count in output:
        print(f"{word} : {count}")
        nbr_word += count
    print(f"Total Words: {nbr_word}")
