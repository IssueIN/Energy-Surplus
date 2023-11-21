import pandas as pd
import argparse
import joblib
from model_training import load_data, prepare_data, split_data
import json
from sklearn.metrics import f1_score

country_code = {
    "SP": 0,  # Spain
    "UK": 1,  # United Kingdom
    "DE": 2,  # Germany
    "DK": 3,  # Denmark
    "HU": 5,  # Hungary
    "SE": 4,  # Sweden
    "IT": 6,  # Italy
    "PO": 7,  # Poland
    "NL": 8   # Netherlands
}

def load_model(model_path):
    return joblib.load(model_path)

def make_predictions(df, model):
    # TODO: Use the model to make predictions on the test data
    X_train, X_val, y_train, y_val = split_data(df)
    return model.predict(X_val), y_val

def save_predictions(predictions, predictions_file):
    # TODO: Save predictions to a JSON file
    predictions_mapped = [country_code[country] for country in predictions]
    predictions_json = {"target": {str(i): pred for i, pred in enumerate(predictions_mapped)}}
    with open(predictions_file, "w") as json_file:
        json.dump(predictions_json, json_file)
    pass

def parse_arguments():
    parser = argparse.ArgumentParser(description='Prediction script for Energy Forecasting Hackathon')
    parser.add_argument(
        '--input_file', 
        type=str, 
        default='data/data.csv', 
        help='Path to the test data file to make predictions'
    )
    parser.add_argument(
        '--model_file', 
        type=str, 
        default='models/model.pkl',
        help='Path to the trained model file'
    )
    parser.add_argument(
        '--output_file', 
        type=str, 
        default='predictions/predictions.json', 
        help='Path to save the predictions'
    )
    return parser.parse_args()

def main(input_file, model_file, output_file):
    df = load_data(input_file)
    df = prepare_data(df)
    model = load_model(model_file)
    predictions, y_test = make_predictions(df, model)
    print("F1 Score:", f1_score(y_test, predictions, average='macro'))
    save_predictions(predictions, output_file)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.model_file, args.output_file)
