import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/home/src/skilled-keyword-292704-secrets.json'
project_id = 'skilled-keyword-292704'

bucket_name = 'mage-zoomcamp-juan-rojas-5'
table_name = 'nyc_taxi_data'

root_path = f'{bucket_name}/{table_name}'
#works at second attempt
@data_exporter
def export_data(data, *args, **kwargs):
    table = pa.Table.from_pandas(data)

    gcs = pa.fs.GcsFileSystem(project_id=project_id)
    
    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['lpep_pickup_date'],
        filesystem=gcs,
        existing_data_behavior = 'overwrite_or_ignore' 
    )

