# ScryDatasets
ScryDatasets is a Python library for managing datasets. It provides a simple interface for uploading, downloading, listing, and deleting datasets.

## Installation

To install ScryDatasets, clone the repository and install the dependencies:

```bash
git clone <repository-url>
cd scry_dataset
pip install -r requirements.txt
```

## Configuration

ScryDatasets can be configured using a YAML file. The library will look for the configuration file in the following locations, in order:

1. `~/.datasetmanager/config.yaml` (User's home directory)
2. `/etc/datasetmanager/config.yaml` (System-wide configuration)
3. `config.yaml` (Current working directory)

You can specify settings such as the default workspace, API keys, and other preferences in this configuration file.

### Sample Configuration

```yaml
storage:
    type: oci
    bucket: ScryDatasets

mongodb:
    database: llm_test_db
    uri: ""
    pem: "/mongo.pem"
    ca: "/rootCA.crt"
```

## Example Usage

```python
import pandas as pd
from ScryDatasets.dataset_manager import DatasetManager

# Create a sample DataFrame
data = {
    'column1': [1, 2, 3],
    'column2': ['a', 'b', 'c']
}
df = pd.DataFrame(data)

# Save the dataset to a CSV file
csv_path = 'sample_dataset.csv'
df.to_csv(csv_path, index=False)

# Initialize DatasetManager
manager = DatasetManager()

# Upload the dataset
dataset_info = manager.upload(csv_path, name='sample_dataset', description='A sample dataset', tags=['example', 'test'])

# List all datasets
datasets = manager.list_datasets()
for ds in datasets:
    print(ds)

# Download the dataset
df = manager.download('sample_dataset')
if df is not None:
    print(df.head())

# Delete the dataset
manager.delete('sample_dataset')
```
