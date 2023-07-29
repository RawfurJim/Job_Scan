import os
import spacy
from src.components.data_ingestion import DataIngestion
from src.components.model_train import ModelTrain
from src.components.model_test import ModelTest

# Directory where models are saved
model_directory = r"C:\Users\HP\Desktop\job_scan\artifact"

def get_latest_model_path():
    """Fetches the latest model based on the versioning in the name"""
    models = [f for f in os.listdir(model_directory) if os.path.isdir(os.path.join(model_directory, f)) and f.startswith('model')]
    models.sort()
    if models:
        return os.path.join(model_directory, models[-1])
    else:
        return None

def main():
    # Initiate the data ingestion, model train and model test classes
    data_ingestion = DataIngestion()
    model_train = ModelTrain()
    model_test = ModelTest(get_latest_model_path())

    # Fetch training and test data
    training_data = data_ingestion.fetch_data('Annotate_data_1')
    test_data = data_ingestion.fetch_test_data()

    # Train a new model
    new_model = model_train.train_model(training_data)

    # Calculate accuracy of the new model
    new_model_accuracy = model_test.evaluate_model(test_data)

    # Get the path of the latest model in the artifact directory
    latest_model_path = get_latest_model_path()
    if latest_model_path:
        # If there is a previous model, load it and calculate its accuracy
        old_model_test = ModelTest(latest_model_path)
        old_model_accuracy = old_model_test.evaluate_model(test_data)
    else:
        # If there is no previous model, set its accuracy as 0
        old_model_accuracy = 0

    # If the new model performs better, save it
    if new_model_accuracy > old_model_accuracy:
        new_version = int(latest_model_path.split('model')[-1]) + 1 if latest_model_path else 1
        new_model_path = os.path.join(model_directory, f'model{new_version}')
        new_model.to_disk(new_model_path)
        print(f"New model saved at {new_model_path} with accuracy {new_model_accuracy:.2f}%")
    else:
        print(f"Old model is better. No new model saved. Old model accuracy: {old_model_accuracy:.2f}%")

if __name__ == "__main__":
    main()

# # Directory where models are saved
# model_directory = r"C:\Users\HP\Desktop\job_scan\artifact"

# def get_latest_model_path():
#     """Fetches the latest model based on the versioning in the name"""
#     models = [f for f in os.listdir(model_directory) if os.path.isdir(os.path.join(model_directory, f)) and f.startswith('model')]
#     models.sort()
#     if models:
#         return os.path.join(model_directory, models[-1])
#     else:
#         return None

# def main():
#     # Fetch training and test data
#     training_data = fetch_data()
#     test_data = fetch_test_data()

#     # Train a new model
#     new_model = train_model(training_data)

#     # Calculate accuracy of the new model
#     new_model_accuracy = evaluate_model(new_model, test_data)

#     # Get the path of the latest model in the artifact directory
#     latest_model_path = get_latest_model_path()
#     if latest_model_path:
#         # If there is a previous model, load it and calculate its accuracy
#         old_model = spacy.load(latest_model_path)
#         old_model_accuracy = evaluate_model(old_model, test_data)
#     else:
#         # If there is no previous model, set its accuracy as 0
#         old_model_accuracy = 0

#     # If the new model performs better, save it
#     if new_model_accuracy > old_model_accuracy:
#         new_version = int(latest_model_path.split('model')[-1]) + 1 if latest_model_path else 1
#         new_model_path = os.path.join(model_directory, f'model{new_version}')
#         new_model.to_disk(new_model_path)
#         print(f"New model saved at {new_model_path} with accuracy {new_model_accuracy:.2f}%")
#     else:
#         print(f"Old model is better. No new model saved. Old model accuracy: {old_model_accuracy:.2f}%")

# if __name__ == "__main__":
#     main()