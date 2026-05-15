import os
from networksecurity.constants import (general, data_ingestion)
from networksecurity.utils.common import read_yaml, create_directories
from networksecurity.entity.config_entity import DataIngestionConfig, DataTransformationConfig
from datetime import datetime

class ConfigurationManager:
    def __init__(self, 
                 config_path=general.CONFIG_FILE_PATH,
                 timestamp=datetime.now()
                 ):
        self.config = read_yaml(path_to_yaml=config_path)
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.artifact_root = os.path.join(general.ARTIFACT_DIR_NAME, timestamp)
        create_directories(paths_to_dir=[self.artifact_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Assign the DataIngestionConfig attribute
        """
        config = self.config.data_ingestion

        # make paths
        data_ingestion_root = os.path.join(self.artifact_root, data_ingestion.ROOT_DIR)
        feature_store_file_path = os.path.join(data_ingestion_root, data_ingestion.FEATURE_STORE_DIR, data_ingestion.RAW_DATA_FILE_NAME)
        train_file_path = os.path.join(data_ingestion_root, data_ingestion.INGESTED_DIR, data_ingestion.TRAIN_FILE_NAME)
        test_file_path = os.path.join(data_ingestion_root, data_ingestion.INGESTED_DIR, data_ingestion.TEST_FILE_NAME)

        data_ingestion_config = DataIngestionConfig(
            root_dir = data_ingestion_root,
            database_name = data_ingestion.DATABASE_NAME, 
            collection_name = data_ingestion.COLLECTION_NAME,
            feature_store_file_path = feature_store_file_path,
            train_file_path = train_file_path,
            test_file_path = test_file_path,
            train_test_split_ratio = config.train_test_split_ratio
        )
        return data_ingestion_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        """
        Assign the DataTransformationConfig attribute
        """
        pass