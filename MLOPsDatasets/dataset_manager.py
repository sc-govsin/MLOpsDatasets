from datetime import datetime, timezone
import ssl
from typing import Optional, List
import logging
from pathlib import Path
import yaml
from pymongo import MongoClient
import oci
import pandas as pd
from .dataset_info import DatasetInfo
from tqdm import tqdm

class DatasetManager:
    """
    A simple interface for managing datasets
    """
    def __init__(self, workspace: Optional[str] = None):
        """
        Initialize DatasetManager
        
        Args:
            workspace: Optional workspace name (defaults to 'default')
        """
        self.workspace = workspace or 'default'
        self._init_workspace()
        self.logger = logging.getLogger(__name__)

    def _init_workspace(self):
        """Initialize the workspace environment"""
        # Create default configuration if it doesn't exist
        self._create_default_config()
        # Load configurations from standard locations
        config_paths = [
            Path.home() / '.datasetmanager/config.yaml',
            Path('/etc/datasetmanager/config.yaml'),
            Path('config.yaml')
        ]
        self._load_config(config_paths)
        self._setup_storage()

    def _create_default_config(self):
        """Create a default configuration file if it doesn't exist"""
        default_config_path = Path.home() / '.datasetmanager/config.yaml'
        if not default_config_path.exists():
            default_config_path.parent.mkdir(parents=True, exist_ok=True)
            default_config = {
                'storage': {
                    'type': 'oci',
                    'bucket': 'your_bucket_name'
                },
                'mongodb': {
                    'uri': 'mongodb://localhost:27017/',
                    'database': 'dataset_manager',
                    'pem': 'path_to_your_mongodb_pem_file',
                    'ca': 'path_to_your_mongodb_ca_file'
                },
                'oci':{
                    'user': 'your_oci_user_ocid',
                    'fingerprint': 'your_oci_fingerprint',
                    'key_file': 'path_to_your_oci_private_key',
                    'tenancy': 'your_oci_tenancy_ocid',
                    'region': 'me-jeddah-1'
                }
            }
            with open(default_config_path, 'w') as f:
                yaml.safe_dump(default_config, f)

    def _load_config(self, config_paths: List[Path]):
        """Load configuration from the first available path"""
        for path in config_paths:
            if path.exists():
                with open(path) as f:
                    self.config = yaml.safe_load(f)
                return
        
        # Use default configuration if no config file found
        self.config = {
            'storage': {
                'type': 'oci',
                'bucket': 'your_bucket_name'
            },
            'mongodb': {
                'uri': 'mongodb://localhost:27017/',
                'database': 'datasets'
            },
            'oci':{
                'user': 'your_oci_user_ocid',
                'fingerprint': 'your_oci_fingerprint',
                'key_file': 'path_to_your_oci_private_key',
                'tenancy': 'your_oci_tenancy_ocid',
                'region': 'me-jeddah-1'
            }
        }
    
    def _connect_db(self):
        # Setup MongoDB connection
        self.mongo_client = MongoClient(self.config['mongodb']['uri'], 
                                        ssl=True, ssl_certfile=self.config['mongodb']['pem'],
                                        ssl_cert_reqs=ssl.CERT_REQUIRED,
                                        tlsCAFile=self.config['mongodb']['ca'])
        self.db = self.mongo_client[self.config['mongodb']['database']]
        self.metadata_collection = self.db['datasets_metadata']

    def _close_db(self):
        self.mongo_client.close()

    def _setup_storage(self):
        """Setup storage backend based on configuration"""
        oci_config = {
            "user": self.config["oci"]["user"],
            "fingerprint": self.config["oci"]["fingerprint"],
            "key_file": self.config["oci"]["key_file"],
            "tenancy": self.config["oci"]["tenancy"],
            "region": self.config["oci"]["region"],
        }
        self.oci_client = oci.object_storage.ObjectStorageClient(
            oci_config
        )
        self.bucket_name = self.config['storage']['bucket']

    def upload(self, dataset_path: str, name: Optional[str] = None, 
               description: Optional[str] = None, tags: Optional[List[str]] = None) -> DatasetInfo:
        """
        Upload a dataset
        
        Args:
            dataset_path: Path to a CSV file
            name: Optional name for the dataset (required if passing a file path)
            description: Optional description of the dataset
            tags: Optional list of tags for the dataset
        
        Returns:
            DatasetInfo object containing dataset metadata
        """
        try:
            self._connect_db()
            # Create unique filename
            timestamp = datetime.now(timezone.utc).isoformat().replace(':', '-')
            
            if name is None:
                name = Path(dataset_path).stem
            filename = name + '_' + timestamp + '.csv'
            # Upload dataset to OCI bucket
            with open(dataset_path, 'rb') as f:
                self.oci_client.put_object(
                    self.oci_client.get_namespace().data,
                    self.bucket_name,
                    filename,
                    f
                )
                # Generate the URL for the uploaded file
                namespace = self.oci_client.get_namespace().data
                url = f"https://objectstorage.{self.config['oci']['region']}.oraclecloud.com/n/{namespace}/b/{self.bucket_name}/o/{filename}"
            
            # Create metadata
            metadata = {
                'name': name,
                'createdOn': timestamp,
                'description': description,
                'fileSize': Path(dataset_path).stat().st_size,
                'tags': tags,
                'fileName': filename,
                'accessLink': url
            }

            # Save metadata to MongoDB
            self.metadata_collection.insert_one(metadata)
            self._close_db()
            return DatasetInfo(**metadata)

        except Exception as e:
            self.logger.error(f"Error uploading dataset: {str(e)}")
            raise

    def download_user_uploaded_data(self, dataset_name: str, output_path: Optional[str] = None) -> None:
        """
        Download a dataset
        
        Args:
            dataset_name: Name of the dataset to download
            output_path: Optional path where to save the CSV file. 
                        If not provided, saves to current working directory.
                        Can be either a directory or a file path.
        """
        try:
            self._connect_db()
            metadata = self.metadata_collection.find_one({'name': dataset_name})
            # Check if dataset exists
            if metadata is None or len(metadata) == 0:
                print(f"Dataset '{dataset_name}' not found")
                return None
            if not metadata:
                raise ValueError(f"Dataset '{dataset_name}' not found")

            if output_path is None:
                 output_path = Path('/tmp') / '.datasetmanager' / 'downloads' / metadata['filename']
            else:
                output_path = Path(output_path)
                if output_path.is_dir():
                    output_path = output_path / metadata['filename']

            obj = self.oci_client.get_object(self.oci_client.get_namespace().data,self.bucket_name, metadata['filename'])
            output_path.parent.mkdir(parents=True, exist_ok=True)
            # with open(output_path, 'wb') as f:
            #     f.write(obj.data.content)
            # Get the total size of the object
            total_size = obj.headers['Content-Length']
            chunk_size = 1024 * 1024  # 1 MB

            # Download the object in chunks and show progress
            with open(output_path, 'wb') as f:
                for chunk in tqdm(obj.data.raw.stream(chunk_size), 
                                  total=int(total_size) // chunk_size, 
                                  unit='MB', 
                                  desc=f"Downloading {dataset_name}"):
                    f.write(chunk)
            # return the pandas dataframe
            self._close_db()
            return pd.read_csv(output_path)

        except Exception as e:
            self.logger.error(f"Error downloading dataset: {str(e)}")
            raise

    def download(self, dataset_name: str, output_path: Optional[str] = None) -> None:
        try:
            obj = self.oci_client.get_object(self.oci_client.get_namespace().data,self.bucket_name, "data/"+dataset_name)
            if output_path is None:
                output_path = Path('/tmp') / '.datasetmanager' / 'downloads' / dataset_name
            else:
                output_path = Path(output_path)
                if output_path.is_dir():
                    output_path = output_path / dataset_name
            output_path.parent.mkdir(parents=True, exist_ok=True)
            # Get the total size of the object
            total_size = obj.headers['Content-Length']
            chunk_size = 1024 * 1024  # 1 MB

            # Download the object in chunks and show progress
            with open(output_path, 'wb') as f:
                for chunk in tqdm(obj.data.raw.stream(chunk_size), 
                                    total=int(total_size) // chunk_size, 
                                    unit='MB', 
                                    desc=f"Downloading {dataset_name}"):
                    f.write(chunk)
            # return the pandas dataframe
            return pd.read_csv(output_path)
        except Exception as e:
            self.logger.error(f"Error downloading dataset: {str(e)}")
            raise e

    def list_datasets(self) -> List[DatasetInfo]:
        """
        List all available datasets in the workspace
        
        Returns:
            List of DatasetInfo objects
        """
        try:
            self._connect_db()
            datasets = []
            for metadata in self.metadata_collection.find():
                datasets.append(DatasetInfo(**metadata))
            self._close_db()
            return sorted(datasets, key=lambda x: x.createdOn, reverse=True)
        except Exception as e:
            self.logger.error(f"Error listing datasets: {str(e)}")
            raise

    def list_datasets_metadata(self) -> List[dict]:
        """
        List all available datasets and their metadata in the workspace
        
        Returns:
            List of dictionaries containing dataset metadata
        """
        try:
            self._connect_db()
            results = list(self.metadata_collection.find())
            self._close_db()
            return results
        except Exception as e:
            self.logger.error(f"Error listing datasets metadata: {str(e)}")
            raise

    def delete(self, dataset_name: str) -> bool:
        """
        Delete a dataset
        
        Args:
            dataset_name: Name of the dataset to delete
        
        Returns:
            Boolean indicating success
        """
        try:
            self._connect_db()
            metadata = self.metadata_collection.find_one({'name': dataset_name})
            if not metadata:
                raise ValueError(f"Dataset '{dataset_name}' not found")

            self.oci_client.delete_object(self.oci_client.get_namespace().data,self.bucket_name, metadata['filename'])
            self.metadata_collection.delete_one({'name': dataset_name})
            self._close_db()
            return True

        except Exception as e:
            self.logger.error(f"Error deleting dataset: {str(e)}")
            raise