import unittest
from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from MLOpsDatasets.dataset_manager import DatasetManager

class TestDatasetManager(unittest.TestCase):

    @patch('MLOpsDatasets.dataset_manager.MongoClient')
    @patch('MLOpsDatasets.dataset_manager.oci.object_storage.ObjectStorageClient')
    def setUp(self, MockOCIClient, MockMongoClient):
        self.mock_oci_client = MockOCIClient.return_value
        self.mock_mongo_client = MockMongoClient.return_value
        self.mock_db = self.mock_mongo_client.__getitem__.return_value
        self.mock_metadata_collection = self.mock_db.__getitem__.return_value
        self.dataset_manager = DatasetManager()

    def test_upload(self):
        with patch('builtins.open', unittest.mock.mock_open(read_data='data')):
            self.dataset_manager.upload('./tests/test.csv', name='test_dataset')
            self.mock_oci_client.put_object.assert_called_once()
            self.mock_metadata_collection.insert_one.assert_called_once()

    def test_download(self):
        self.mock_metadata_collection.find_one.return_value = {'name': 'test_dataset', 'fileName': 'test.csv'}
        with patch('builtins.open', unittest.mock.mock_open()), patch('pandas.read_csv'):
            self.dataset_manager.download('test_dataset')
            self.mock_oci_client.get_object.assert_called_once()

    def test_list_datasets_metadata(self):
        self.mock_metadata_collection.find.return_value = [{'name': 'test_dataset', 'fileName': 'test.csv'}]
        result = self.dataset_manager.list_datasets_metadata()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'test_dataset')

    def test_download_user_uploaded_data(self):
        self.mock_metadata_collection.find_one.return_value = {'name': 'test_dataset', 'fileName': 'test.csv'}
        with patch('builtins.open', unittest.mock.mock_open()), patch('pandas.read_csv'):
            self.dataset_manager.download_user_uploaded_data('test_dataset')
            self.mock_oci_client.get_object.assert_called_once()

    def test_delete(self):
        self.mock_metadata_collection.find_one.return_value = {'name': 'test_dataset', 'fileName': 'test.csv'}
        self.dataset_manager.delete('test_dataset')
        self.mock_metadata_collection.delete_one.assert_called_once()

if __name__ == '__main__':
    unittest.main()