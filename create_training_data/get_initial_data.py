import spacy
import pandas as pd
from sqlalchemy import create_engine, Table, Column, String, MetaData, Text
from pymongo import MongoClient
from sqlalchemy import create_engine
import urllib
import pyodbc
import json
import spacy
from src.components.data_ingestion import fetch_data, fetch_test_data
from src.components.model_train import train_model
from src.components.model_test import evaluate_model
from datetime import datetime
import os

# # Establish a connection to the SQL Server
# params = urllib.parse.quote_plus(r'DRIVER={SQL Server};SERVER=HP-ELITEBOOK\SQLEXPRESS;DATABASE=job_scan;Trusted_Connection=yes;')
# engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

# # Load the spaCy model
# nlp = spacy.load(r"C:\Users\HP\Desktop\job_scan\artifact\spacy_model")


# # Establish a connection to the SQL Server
# params = urllib.parse.quote_plus(r'DRIVER={SQL Server};SERVER=HP-ELITEBOOK\SQLEXPRESS;DATABASE=job_scan;Trusted_Connection=yes;')
# engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

# # Load the spaCy model
# nlp = spacy.load(r"C:\Users\HP\Desktop\job_scan\artifact\spacy_model")

# # MongoDB Connection
# client = MongoClient('mongodb://localhost:27017/')
# db = client['job_db']  # Use your desired database
# collection = db['pre_annotate_data']  # Use your desired collection


def fetch_data_from_sql(engine):
    """
    Function to fetch data from SQL database
    """
    data = []
    df = pd.read_sql('SELECT * FROM job_data', engine)
    for i in df['job_description']:
        data.append(i)
    a = ''.join(data)
    return a

def process_data_through_spacy(data, nlp):
    """
    Function to process data through the spaCy model
    """
    annotations = []

    doc = nlp(data)
        
        # Extract annotations
    entities = [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
        
        # Append to annotations list
    annotations.append({"text": data, "entities": entities})
    return annotations

def save_to_local_directory(annotations, directory):
    os.makedirs(directory, exist_ok=True)

    # Use current date and time to create a unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"annotations_{timestamp}.json"
    filepath = os.path.join(directory, filename)

    with open(filepath, 'w') as f:
        json.dump(annotations, f)

def insert_into_mongodb(annotations, collection):
    """
    Function to insert data into MongoDB
    """
    # Insert annotations into MongoDB
    for annotation in annotations:
        collection.insert_one(annotation)

# df = fetch_data_from_sql(engine)
# annotations = process_data_through_spacy(df, nlp)
# save_to_local_directory(annotations, r'C:\Users\HP\Desktop\job_scan\pre_anootate_data')
# insert_into_mongodb(annotations, collection)


