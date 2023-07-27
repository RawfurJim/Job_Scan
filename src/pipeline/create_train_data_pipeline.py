import spacy
import pandas as pd
from sqlalchemy import create_engine, Table, Column, String, MetaData, Text
from pymongo import MongoClient
from sqlalchemy import create_engine
import urllib
import pyodbc
import json
import spacy
from create_training_data.get_initial_data import fetch_data_from_sql, process_data_through_spacy,insert_into_mongodb,save_to_local_directory
from src.components.model_train import train_model
from src.components.model_test import evaluate_model

# Establish a connection to the SQL Server
params = urllib.parse.quote_plus(r'DRIVER={SQL Server};SERVER=HP-ELITEBOOK\SQLEXPRESS;DATABASE=job_scan;Trusted_Connection=yes;')
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

# Load the spaCy model
nlp = spacy.load(r"C:\Users\HP\Desktop\job_scan\artifact\spacy_model")

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['job_db']  # Use your desired database
collection = db['pre_annotate_data']  # Use your desired collection


df = fetch_data_from_sql(engine)
annotations = process_data_through_spacy(df, nlp)
save_to_local_directory(annotations, r'C:\Users\HP\Desktop\job_scan\pre_anootate_data')
insert_into_mongodb(annotations, collection)


