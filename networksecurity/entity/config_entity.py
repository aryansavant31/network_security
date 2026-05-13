from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    collection_name: str
    database_name: str
    feature_store_file_path: Path
    train_file_path: Path
    test_file_path: Path
    train_test_split_ratio: float

@dataclass
class DataTransformationConfig:
    root_dir: Path