# MLOpsDatasets
## Overview
`MLOpsDatasets` is a Python library that allows users to easily manage datasets created on the IoT-Sense platform. Users can download datasets they have created, list available datasets, and delete user-uploaded files.

## Installation

To install MLOpsDatasets, clone the repository and install the dependencies:

```bash
git clone <repository-url>
cd scry_dataset
pip install -r requirements.txt
```
or 
```
pip install git+https://github.com/sc-govsin/MLOpsDatasets.git@v1.1.3
```
## Configuration

MLOpsDatasets can be configured using a YAML file. The library will look for the configuration file in the following locations, in order:

1. `~/.datasetmanager/config.yaml` (User's home directory)
2. `/etc/datasetmanager/config.yaml` (System-wide configuration)
3. `config.yaml` (Current working directory)

You can specify settings such as the default workspace, API keys, and other preferences in this configuration file.

### Sample Configuration

```yaml
storage:
    type: oci
    bucket: MLOpsDatasets

mongodb:
    database: llm_test_db
    uri: ""
    pem: "/mongo.pem"
    ca: "/rootCA.crt"
oci:
  user: 
  fingerprint: 
  key_file: key.pem
  tenancy: 
  region: 
```

## Example Usage

### Downloading Datasets Created on IoT-Sense Platform
```python
import pandas as pd
from MLOpsDatasets.dataset_manager import DatasetManager

# Initialize DatasetManager
manager = DatasetManager()

# Download the dataset created from the IoT-platform
# Replace 'Dataset_ABC_28-02-2025T10_55_31' with the actual dataset name

df = manager.download('Dataset_ABC_28-02-2025T10_55_31')
if df is not None:
    print(df.head())
else:
    print("Dataset not found or could not be downloaded.")
```

### Additional Features

#### Uploading a Dataset (Deprecated)
```python
# Create a sample DataFrame
data = {
    'column1': [1, 2, 3],
    'column2': ['a', 'b', 'c']
}
df = pd.DataFrame(data)

# Save the dataset to a CSV file
csv_path = 'sample_dataset.csv'
df.to_csv(csv_path, index=False)

# Upload the dataset
manager = DatasetManager()
dataset_info = manager.upload(csv_path, name='sample_dataset', description='Sample dataset', tags=['sample'])
```

#### Listing All Datasets
```python
datasets = manager.list_datasets()
for ds in datasets:
    print(ds)
```

#### Downloading User-Uploaded Datasets (Deprecated)
```python
df = manager.download_user_uploaded_data('sample_dataset')
```

#### Deleting a Dataset
```python
# Only user-uploaded datasets can be deleted
manager.delete('sample_dataset')
```

## Notes
- **Dataset downloads from the IoT-Sense platform**: Ensure you use the correct dataset name.
- **Deprecation Notice**: The `upload()` and `download_user_uploaded_data()` methods are deprecated.
- **Deletion**: You can only delete datasets that you have uploaded.
