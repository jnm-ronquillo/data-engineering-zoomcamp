-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `skilled-keyword-292704.nytaxi.external_green_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://skilled-keyword-292704-nyc-tl-data/green/green_tripdata_2022-*.parquet']
);

-- Check green trip data
SELECT * FROM skilled-keyword-292704.nytaxi.external_green_tripdata limit 10;

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE skilled-keyword-292704.nytaxi.green_tripdata_non_partitoned AS
SELECT * FROM skilled-keyword-292704.nytaxi.external_green_tripdata;

--Count number of records
SELECT COUNT(1) FROM skilled-keyword-292704.nytaxi.green_tripdata_non_partitoned;

-- Impact of materialized table
-- Scanning 0 MB (cached) of data
SELECT DISTINCT(PULocationID)
FROM skilled-keyword-292704.nytaxi.external_green_tripdata;

-- Scanning 6.41 MB of data
SELECT DISTINCT(PULocationID)
FROM skilled-keyword-292704.nytaxi.green_tripdata_non_partitoned;

--Count number of records with fare_amount 0
SELECT COUNT(1) FROM skilled-keyword-292704.nytaxi.green_tripdata_non_partitoned
WHERE fare_amount = 0;

-- Create a partitioned and clustered table from external table
CREATE OR REPLACE TABLE skilled-keyword-292704.nytaxi.green_tripdata_partitoned_clustered
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PUlocationID AS
SELECT * FROM skilled-keyword-292704.nytaxi.external_green_tripdata;

-- Impact of partitioned table
-- Scanning 12.82 MB of data
SELECT DISTINCT(PULocationID)
FROM skilled-keyword-292704.nytaxi.green_tripdata_non_partitoned
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';

-- Scanning 1.12 MB of data
SELECT DISTINCT(PULocationID)
FROM skilled-keyword-292704.nytaxi.green_tripdata_partitoned_clustered
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';
