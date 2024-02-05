import pandas as pd
import numpy as np   
import re
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    print("Rows with empty NaN passengers", pd.isna(data['passenger_count']).sum())
    print("Rows with empty NaN trip distance", pd.isna(data['trip_distance']).sum())
    print("Rows with no passengers or zero trip distance:", ((data['passenger_count'].isna() | data['passenger_count'].isin([0])) | data['trip_distance'].isin([0])).sum())
    
    # Count columns with camel case names
    camel_case_pattern = re.compile(r'^[A-Z][a-zA-Z]*$')
    camel_case_columns = [col for col in data.columns if camel_case_pattern.match(col)]
    print('columns camel case number',len(camel_case_columns))
    print('columns camel case',camel_case_columns)

    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    # Rename columns from camel case to snake case
    data.columns = data.columns.str.replace(r'([a-z])([A-Z])', r'\1_\2').str.lower()

    return data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]


@test
def test_output(data) -> None:
    """
    Template code for testing the output of the block.
    """
    assert data is not None, 'The output is undefined'

    assert 'vendor_id' in data.columns, 'The column vendor_id does not exists'
    #print('filas',data.shape[0])
    #print('passenger_count cero',(data['passenger_count']== 0).sum())
    assert (data['passenger_count'] > 0).sum() == data.shape[0] , 'There are no passenger_count rows'
    assert (data['trip_distance'] > 0).sum() == data.shape[0] , 'There are zero trip_distance rows'