import os
import sys
import pandas as pd
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

@dataclass
class DataIngesConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngesConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # Corrected file path using raw string
            file_path = r'notebook\data\stud.csv'  
            print(f"Reading dataset from: {file_path}")  # Debugging

            df = pd.read_csv(file_path)
            logging.info('Read the dataset as dataframe')

            # Ensure artifacts directory exists
            artifacts_dir = os.path.dirname(self.ingestion_config.train_data_path)
            print(f"Creating artifacts directory: {artifacts_dir}")  # Debugging
            os.makedirs(artifacts_dir, exist_ok=True)

            # Save raw data
            print(f"Saving raw data to: {self.ingestion_config.raw_data_path}")  # Debugging
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train-test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Save train and test data (Fixed `tocsv()` -> `to_csv()`)
            print(f"Saving train data to: {self.ingestion_config.train_data_path}")  # Debugging
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)

            print(f"Saving test data to: {self.ingestion_config.test_data_path}")  # Debugging
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    obj = DataIngestion()
    train_data,test_data= obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    data_transformation.initiate_data_transformation(train_data,test_data)