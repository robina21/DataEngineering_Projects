Project Description:
This project is an ETL (Extract, Transform, Load) pipeline that collects tweets from the Twitter API, transforms the data, and loads it into a PostgreSQL database. The pipeline is designed to run every 10 minutes and update the database with the latest tweets.

Tools Used:

Python 3
Tweepy (Python library for accessing Twitter API)
PostgreSQL (relational database management system)
SQLAlchemy (Python library for database connection and manipulation)
Project Structure:

main.py: the main script that runs the ETL pipeline
config.py: configuration file for API keys and database connection details
requirements.txt: file containing required Python libraries
README.md: documentation for the project
ETL Pipeline Steps:

Extract: Access the Twitter API using Tweepy and retrieve the latest tweets based on specified search keywords.
Transform: Clean and preprocess the tweets by removing stop words, special characters, and URLs. Then, extract relevant information from the tweets such as text, user handle, timestamp, and number of likes and retweets.
Load: Establish a connection with the PostgreSQL database using SQLAlchemy and insert the transformed data into a table.
Potential Future Improvements:

Add error handling and logging to the pipeline
Use a scheduler (e.g., Apache Airflow) to automate the pipeline on a larger scale
Expand the pipeline to collect data from other social media platforms such as Instagram and Facebook
