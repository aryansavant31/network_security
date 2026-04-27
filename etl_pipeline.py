import sys
import os
import certifi
import pandas as pd
import json
from networksecurity.exceptions.custom_exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from typing import List
import pymongo
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")

ca = certifi.where() # ca = certificate authority. With this, any external connection looks legit from our side

class ETLPipeline:
    def csv_to_json(self, filepath:Path) -> list:
        try:    
            # EXTRACT the csv file
            data = pd.read_csv(filepath)

            # TRANSFORM csv file
            # remove index
            data.reset_index(drop=True, inplace=True)

            # convert from dataframe to json
            records = list(json.loads(data.T.to_json()).values())
            logger.info("csv file converted to list of jsons")
            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def upload_data_to_mongodb(self, records:list, collection:str, database:str):
        try:
            mongodb_client = pymongo.MongoClient(host=MONGO_DB_URI)

            # LOAD data to mongodb server
            database = mongodb_client[database]
            collection = database[collection]
            collection.insert_many(records)
            logger.info("Network data uploaded to Mongodb server")
            logger.info(f"Number of records are: {len(records)}")

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__ == "__main__":
    FILEPATH = Path("network_data/phisingData.csv")
    DATABASE = "AryanSavant"
    collection = "NetworkData"

    etl_obj = ETLPipeline()
    records = etl_obj.csv_to_json(filepath=FILEPATH)
    etl_obj.upload_data_to_mongodb(records, collection, DATABASE)
