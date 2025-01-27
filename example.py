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
# df.to_csv(csv_path, index=False)

# Initialize DatasetManager
manager = DatasetManager()

# Upload the dataset
dataset_info = manager.upload(csv_path, name='sample_dataset', description='A sample dataset', tags=['example', 'test'])

# List all datasets
datasets = manager.list_datasets()
for ds in datasets:
    print(ds)

# Download the dataset
manager.download('sample_dataset', output_path='downloaded_sample_dataset.csv')

# Delete the dataset
# manager.delete('sample_dataset')
