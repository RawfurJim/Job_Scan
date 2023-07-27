

import spacy
from src.components.data_ingestion import fetch_test_data
import re


def evaluate_model(nlp, test_data):

    def preprocess_text(text):
        text = re.sub('\s+', ' ', text)
        text = text.strip()
        return text

    # Initialize counters for correctly recognized entities and total entities
    correct_entities = 0
    total_entities = 0

    for text, annotations in test_data:
        text = preprocess_text(text)
        print(text)

        # Get the original words that are entities
        original_entities = [text[start:end] for start, end, label in annotations['entities']]

        # Update total_entities
        total_entities += len(original_entities)

        # Predict entities using the model
        doc = nlp(text)

        # Get the words that the model predicts as entities
        predicted_entities = [ent.text for ent in doc.ents]

        # Check how many entities are correctly predicted
        correct_entities += len([entity for entity in original_entities if entity in predicted_entities])
        for ent in doc.ents:
            print(ent.text, ent.label_)

    # Calculate the accuracy
    accuracy = correct_entities / total_entities * 100
    print(accuracy)
    return accuracy

if __name__ == "__main__":
    nlp = spacy.load(r"C:\Users\HP\Desktop\job_scan\artifact\spacy_model")
    test_data = fetch_test_data()
    acc = evaluate_model(nlp , test_data)




   
