
import unittest
from unittest.mock import patch, MagicMock
from ScryDatasets.dataset_manager import DatasetManager

class TestDatasetManager(unittest.TestCase):

    @patch('ScryDatasets.dataset_manager.MongoClient')
    @patch('ScryDatasets.dataset_manager.oci.object_storage.ObjectStorageClient')
    def setUp(self, MockOCIClient, MockMongoClient):
        self.mock_oci_client = MockOCIClient.return_value
        self.mock_mongo_client = MockMongoClient.return_value
        self.mock_db = self.mock_mongo_client.__getitem__.return_value
        self.mock_metadata_collection = self.mock_db.__getitem__.return_value
        self.dataset_manager = DatasetManager()

    def test_upload(self):
        with patch('builtins.open', unittest.mock.mock_open(read_data='data')):
            self.dataset_manager.upload('test.csv', name='test_dataset')
            self.mock_oci_client.put_object.assert_called_once()
            self.mock_metadata_collection.insert_one.assert_called_once()

    def test_download(self):
        self.mock_metadata_collection.find_one.return_value = {'name': 'test_dataset', 'filename': 'test.csv'}
        with patch('builtins.open', unittest.mock.mock_open()), patch('pandas.read_csv'):
            self.dataset_manager.download('test_dataset')
            self.mock_oci_client.get_object.assert_called_once()

    def test_list_datasets_metadata(self):
        self.mock_metadata_collection.find.return_value = [{'name': 'test_dataset'}]
        result = self.dataset_manager.list_datasets_metadata()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'test_dataset')

if __name__ == '__main__':
    unittest.main()