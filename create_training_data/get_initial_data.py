import spacy
import pandas as pd
from sqlalchemy import create_engine, Table, Column, String, MetaData, Text
from pymongo import MongoClient
from sqlalchemy import create_engine
import urllib
import pyodbc
import json
import spacy
from datetime import datetime
import os



class DataFetcher:
    def __init__(self, engine, nlp, collection):
        self.engine = engine
        self.nlp = nlp
        self.collection = collection

    def fetch_data_from_sql(self):
        """
        Function to fetch data from SQL database
        """
        try:
            data = []
            df = pd.read_sql('SELECT * FROM job_data', self.engine)
            for i in df['job_description']:
                data.append(i)
            a = ''.join(data)
            return a
        except Exception as e:
            logging.error("Error occurred while fetching data from SQL", exc_info=True)
            raise CustomException(e, sys.exc_info())

    def process_data_through_spacy(self, data):
        """
        Function to process data through the spaCy model
        """
        try:
            annotations = []
            doc = self.nlp(data)
            entities = [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
            annotations.append({"text": data, "entities": entities})
            return annotations
        except Exception as e:
            logging.error("Error occurred while processing data through SpaCy", exc_info=True)
            raise CustomException(e, sys.exc_info())

    def converted_data(self, data):
        converted_data = []
        for index, item in enumerate(data):
            new_item = {}
            new_item["id"] = index + 1
            new_item["text"] = item["text"]
            new_item["label"] = [[entity[1], entity[2], entity[3]] for entity in item["entities"]]
            new_item["Comments"] = []  # add this if your output also requires the "Comments" field
            converted_data.append(new_item)
        return converted_data

    def save_to_local_directory(self, annotations, directory):
        try:
            data = self.converted_data(annotations)
            os.makedirs(directory, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"annotations_{timestamp}.jsonl"
            filepath = os.path.join(directory, filename)
            with open(filepath, 'w') as f:
                for item in data:
                    json.dump(item, f)
                    f.write('\n')
        except Exception as e:
            logging.error("Error occurred while saving data to local directory", exc_info=True)
            raise CustomException(e, sys.exc_info())

    def insert_into_mongodb(self, annotations):
        """
        Function to insert data into MongoDB
        """
        try:
            data = self.converted_data(annotations)
            for annotation in data:
                self.collection.insert_one(annotation)
        except Exception as e:
            logging.error("Error occurred while inserting data into MongoDB", exc_info=True)
            raise CustomException(e, sys.exc_info())


# def fetch_data_from_sql(engine):
#     """
#     Function to fetch data from SQL database
#     """
#     data = []
#     df = pd.read_sql('SELECT * FROM job_data', engine)
#     for i in df['job_description']:
#         data.append(i)
#     a = ''.join(data)
#     return a

# def process_data_through_spacy(data, nlp):
#     """
#     Function to process data through the spaCy model
#     """
#     annotations = []

#     doc = nlp(data)
        
#         # Extract annotations
#     entities = [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
        
#         # Append to annotations list
#     annotations.append({"text": data, "entities": entities})
#     return annotations

# # To make sure Docanno can understand the file we ned to convert the file formet

# def converted_data(data):
#     converted_data = []

#     for index, item in enumerate(data):
#         new_item = {}
#         new_item["id"] = index + 1
#         new_item["text"] = item["text"]

#         # Remove the text segment from each entity
#         new_item["label"] = [[entity[1], entity[2], entity[3]] for entity in item["entities"]]

#         new_item["Comments"] = []  # add this if your output also requires the "Comments" field
#         converted_data.append(new_item)

#     return converted_data

# def save_to_local_directory(annotations, directory):
#     data = converted_data(annotations)
#     os.makedirs(directory, exist_ok=True)

#     # Use current date and time to create a unique filename
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"annotations_{timestamp}.jsonl"
#     filepath = os.path.join(directory, filename)
#     with open(filepath, 'w') as f:  # replace 'newfile.jsonl' with your desired filename
#         for item in data:
#             json.dump(item, f)
#             f.write('\n')

#     # with open(filepath, 'w') as f:
#     #     json.dump(annotations, f)

# def insert_into_mongodb(annotations, collection):
#     data = converted_data(annotations)
#     """
#     Function to insert data into MongoDB
#     """
#     # Insert annotations into MongoDB
#     for annotation in data:
#         collection.insert_one(annotation)

