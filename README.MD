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

### [requirements.txt](file:///c%3A/Users/govind_singh/Documents/scry_dataset/requirements.txt)

```plaintext
pandas
pyyaml
```

## Example Usage

```python
import pandas as pd
from ScryDatasets import Dataset
from ScryDatasets import DatasetManager

# Create a DataFrame
data = {'column1': [1, 2, 3], 'column2': [4, 5, 6]}
df = pd.DataFrame(data)

# Create a Dataset
dataset = Dataset(df, name='example_dataset', description='An example dataset', tags=['example', 'test'])

# Initialize DatasetManager
manager = DatasetManager(workspace='my_workspace')

# Upload the dataset
info = manager.upload(dataset)
print(info)
```

# Download the dataset
```python
downloaded_dataset = manager.download('example_dataset')
print(downloaded_dataset.df)
```

# List all datasets
```python
datasets = manager.list_datasets()
for dataset_info in datasets:
    print(dataset_info)
```
# Delete a dataset
```python
success = manager.delete('example_dataset')
print(success)
```