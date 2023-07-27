import spacy
import pickle
from spacy.training import Example
import random
from spacy.training import offsets_to_biluo_tags

from src.components.data_ingestion import fetch_data, fetch_test_data


def train_model(data):
   
    # Load the existing model
    nlp = spacy.load("en_core_web_sm")

    # Get the NER pipeline component
    ner = nlp.get_pipe("ner")

    # Add labels
    for _, annotations in data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # Disable other components for efficient training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes): 
        # Only train NER
        optimizer = nlp.resume_training()

        # Create a list of examples
        examples = [Example.from_dict(nlp.make_doc(text), annotations) for text, annotations in data]

        # Train for 60 iterations
        for itn in range(60):
            random.shuffle(examples)
            losses = {}
            for batch in spacy.util.minibatch(examples, size=2):
                nlp.update(batch, sgd=optimizer, losses=losses)
            print(losses)

    # Instead of saving the model to disk here, we return it
    return nlp

if __name__=="__main__":
    train_data = fetch_data()
    train_model(train_data)









# from spacy.training import offsets_to_biluo_tags

# # Load the existing model
# nlp = spacy.load("en_core_web_sm")

# # Get the NER pipeline component
# ner = nlp.get_pipe("ner")

# data = fetch_data()

# # Add labels
# for _, annotations in data:
#     for ent in annotations.get("entities"):
#         ner.add_label(ent[2])

# # Disable other components for efficient training
# other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
# with nlp.disable_pipes(*other_pipes): 
#     # Only train NER
#     optimizer = nlp.resume_training()

#     # Create a list of examples
#     examples = [Example.from_dict(nlp.make_doc(text), annotations) for text, annotations in data]

#     # Train for 150 iterations
#     for itn in range(60):
#         random.shuffle(examples)
#         losses = {}
#         for batch in spacy.util.minibatch(examples, size=2):
#             nlp.update(batch, sgd=optimizer, losses=losses)
#         print(losses)



# nlp.to_disk(r"C:\Users\HP\Desktop\job_scan\artifact\spacy_model")






