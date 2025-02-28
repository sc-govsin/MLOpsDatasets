"""
This script demonstrates the usage of the ScryDatasets library to manage datasets.
The script performs the following operations:
1. Creates a sample DataFrame.
2. Saves the DataFrame to a CSV file (commented out).
3. Initializes the DatasetManager.
4. Uploads the dataset to the manager (deprecated method).
5. Lists all datasets managed by the DatasetManager.
6. Downloads a user-uploaded dataset (deprecated method).
7. Downloads a dataset created from the IOT-platform.
8. Deletes a user-uploaded dataset.
Dependencies:
- pandas
- ScryDatasets
Note: Some methods used in this script are deprecated.
"""
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

# Upload the dataset : Deprecated
dataset_info = manager.upload(csv_path, name='sample_dataset', description='sample_dataset', tags=['tessample_datasett'])

# List all datasets
datasets = manager.list_datasets()
for ds in datasets:
    print(ds)

# Download user created datasets : Deprecated
df = manager.download_user_uploaded_data('sample_dataset')

# Download the dataset created from the IOT-platform
df = manager.download('Dataset_ABC_28-02-2025T10_55_31')
if df is not None:
    print(df.head())
else:
    print(df)

# Delete the dataset Only user uploaed files will get deleted with this method
manager.delete('sample_dataset')