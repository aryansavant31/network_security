from networksecurity.components.data_ingestion import DataIngestionComponent
from networksecurity.manager.configuration import ConfigurationManager
from networksecurity.logging.logger import logger
from networksecurity.exceptions.custom_exception import NetworkSecurityException
import sys
import os

class TrainingPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()

    def data_ingestion(self):
        try:
            logger.info("Starting data ingestion")
            data_ingestion_config = self.config_manager.get_data_ingestion_config()
            data_ingestion_comp = DataIngestionComponent(config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion_comp.initiate_data_ingestion()
            logger.info("Complete data ingestion")
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)