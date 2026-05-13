from box.exceptions import BoxValueError
from box import ConfigBox
import json
import joblib
from pathlib import Path
from typing import Any
import os
import yaml
from networksecurity.logging.logger import logger

def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Parameters
    -----------
    path_to_yaml: Path
        path to the .yaml file
    """
    try:
        with open(path_to_yaml) as yaml_file:
            params = ConfigBox(yaml.safe_load(yaml_file))
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return params
    except BoxValueError:
        raise ValueError("Yaml file is empty")
    except Exception as e:
        raise e
    

def create_directories(paths_to_dir: list, verbose=True):
    for path in paths_to_dir:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Creating directory at {path}")