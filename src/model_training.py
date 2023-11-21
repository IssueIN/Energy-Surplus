import pandas as pd
import argparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import joblib

def load_data(file_path):
    df = pd.read_csv(file_path)
    df['StartTime'] = pd.to_datetime(df['StartTime'])
    return df

def prepare_data(df):
    # Calculate surplus for each country
    for country in ['DE', 'DK', 'HU', 'IT', 'NE', 'PO', 'SE', 'SP', 'UK']:
        df[f'surplus_{country}'] = df[f'green_energy_{country}'] - df[f'{country}_Load']
    
    # Identify the country with the maximum surplus
    surplus_cols = [col for col in df.columns if 'surplus_' in col]
    df['max_surplus_country'] = df[surplus_cols].idxmax(axis=1).str.replace('surplus_', '')

    return df

def split_data(df):
    # TODO: Split data into training and validation sets (the test set is already provided in data/test_data.csv)
    X = df[[col for col in df.columns if col.startswith('surplus_')]]
    y = df['max_surplus_country']
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, shuffle=False)
    return X_train, X_val, y_train, y_val

def train_model(X, y):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def save_model(model, model_path):
    joblib.dump(model, model_path)
    pass

def parse_arguments():
    parser = argparse.ArgumentParser(description='Model training script for Energy Forecasting Hackathon')
    parser.add_argument(
        '--input_file', 
        type=str, 
        default='data/data.csv', 
        help='Path to the processed data file to train the model'
    )
    parser.add_argument(
        '--model_file', 
        type=str, 
        default='models/model.pkl', 
        help='Path to save the trained model'
    )
    return parser.parse_args()

def main(input_file, model_file):
    df = load_data(input_file)
    df = prepare_data(df)
    X_train, X_val, y_train, y_val = split_data(df)
    model = train_model(X_train, y_train)
    save_model(model, model_file)
    print

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.model_file)