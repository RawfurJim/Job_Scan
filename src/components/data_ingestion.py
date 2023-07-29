from pymongo import MongoClient
import pandas as pd
import time
from src.exception import CustomException
from src.logger import logging

class DataIngestion:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['job_db']

    def fetch_data(self, collection_name):
        try:
            collection = self.db[collection_name]
            data = list(collection.find({}))
            df = pd.DataFrame(data)
            data = []
            for i in range(len(df)):
                text = df.iloc[i]['text']
                entities = df.iloc[i]['label']
                data.append((text, {"entities": entities}))
            clean_data = self.remove_overlapping_entities(data)
            return clean_data
        except Exception as e:
            logging.error(CustomException(e, sys.exc_info()))
            raise CustomException(e, sys.exc_info())

    def fetch_test_data(self):
        return self.fetch_data('test_data')

    def remove_overlapping_entities(self, data):
        try:
            result = []
            for text, annot in data:
                entities = sorted(annot["entities"], key=lambda x: x[0]) # Sort entities by start character
                non_overlapping_entities = []
                prev_entity = entities[0]
                for curr_entity in entities[1:]:
                    # If the start of current entity is inside the previous entity span, it is an overlap
                    if curr_entity[0] < prev_entity[1]:
                        # Take the longer entity
                        if (curr_entity[1]-curr_entity[0]) > (prev_entity[1]-prev_entity[0]):
                            prev_entity = curr_entity
                    else:
                        non_overlapping_entities.append(prev_entity)
                        prev_entity = curr_entity
                non_overlapping_entities.append(prev_entity) # add the last entity
                result.append((text, {"entities": non_overlapping_entities}))
            return result
            pass
        except Exception as e:
            logging.error(CustomException(e, sys.exc_info()))
            raise CustomException(e, sys.exc_info())

if __name__=="__main__":
    data_ingest = DataIngestion()
    data_ingest.fetch_data('Annotate_data_1')
    data_ingest.fetch_test_data()


# def fetch_data():
#     # Create a client
#     client = MongoClient('mongodb://localhost:27017/')

# # Connect to your database
#     db = client['job_db']
#     # Get your collection
#     collection = db['Annotate_data_1']

#     # Fetch all documents from your collection
#     data = list(collection.find({}))

#     # Convert data to pandas DataFrame
#     df = pd.DataFrame(data)
#     data = []
#     for i in range(len(df)):
#         text = df.iloc[i]['text']
#         entities = df.iloc[i]['label']
#         data.append((text, {"entities": entities}))
#     clean_data = remove_overlapping_entities(data)
#     return clean_data

# def fetch_test_data():
#     client = MongoClient('mongodb://localhost:27017/')
#     db = client['job_db']
#     collection = db['test_data']  # use your test data collection
#     data = list(collection.find({}))
#     df = pd.DataFrame(data)
#     data = []
#     for i in range(len(df)):
#         text = df.iloc[i]['text']
#         entities = df.iloc[i]['label']
#         data.append((text, {"entities": entities}))
#     clean_data = remove_overlapping_entities(data)
   
#     return clean_data

# def remove_overlapping_entities(data):
#     result = []
#     for text, annot in data:
#         entities = sorted(annot["entities"], key=lambda x: x[0]) # Sort entities by start character
#         non_overlapping_entities = []
#         prev_entity = entities[0]
#         for curr_entity in entities[1:]:
#             # If the start of current entity is inside the previous entity span, it is an overlap
#             if curr_entity[0] < prev_entity[1]:
#                 # Take the longer entity
#                 if (curr_entity[1]-curr_entity[0]) > (prev_entity[1]-prev_entity[0]):
#                     prev_entity = curr_entity
#             else:
#                 non_overlapping_entities.append(prev_entity)
#                 prev_entity = curr_entity
#         non_overlapping_entities.append(prev_entity) # add the last entity
#         result.append((text, {"entities": non_overlapping_entities}))
#     return result
# if __name__=="__main__":
#     fetch_data()
#     fetch_test_data()