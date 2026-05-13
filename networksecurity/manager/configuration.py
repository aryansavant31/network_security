import os
from networksecurity.constants import (general, data_ingestion)
from networksecurity.utils.common import read_yaml, create_directories
from networksecurity.entity.config_entity import DataIngestionConfig, DataTransformationConfig

class ConfigurationManager:
    def __init__(self, config_path=general.CONFIG_FILE_PATH):
        self.config = read_yaml(path_to_yaml=config_path)
        create_directories(path_to_dir=[general.ARTIFACT_DIR])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Assign the DataIngestionConfig attribute
        """
        config = self.config.data_ingestion

        # make paths
        data_ingestion_root = os.path.join(general.ARTIFACT_DIR, data_ingestion.ROOT_DIR)
        feature_store_file_path = os.path.join(data_ingestion_root, data_ingestion.FEATURE_STORE_DIR)
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