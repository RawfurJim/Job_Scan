

import spacy
import re
import os

class PredictPipeline:

    def __init__(self):
        model_path = os.path.join('artifact', 'spacy_model')
        self.nlp = spacy.load(model_path)

    def evaluate_model(self, text):
        doc = self.nlp(text)
        results = [(ent.text, ent.label_) for ent in doc.ents]
        return results 