

import spacy
from src.components.data_ingestion import fetch_test_data
import re

class PredictPipeline:

    def __init__(self):
        self.nlp = spacy.load(r"C:\Users\HP\Desktop\job_scan\artifact\spacy_model")

    def evaluate_model(self, text):
        doc = self.nlp(text)
        results = [(ent.text, ent.label_) for ent in doc.ents]
        return results