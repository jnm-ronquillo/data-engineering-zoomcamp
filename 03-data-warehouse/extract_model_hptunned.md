## Model deployment
[Tutorial](https://cloud.google.com/bigquery-ml/docs/export-model-tutorial)
### Steps
- gcloud auth login
- bq --project_id skilled-keyword-292704 extract -m nytaxi.tip_hyperparam_model gs://skilled-keyword-292704_taxi_ml_model/tip_hyperparam_model
- mkdir /tmp/model
- gsutil cp -r gs://skilled-keyword-292704_taxi_ml_model/tip_hyperparam_model /tmp/model
- mkdir -p serving_dir/tip_hyperparam_model/1
- cp -r /tmp/model/tip_hyperparam_model/* serving_dir/tip_hyperparam_model/1
# Docker image for Mac ARM 
[Source](https://github.com/emacski/tensorflow-serving-arm)
- docker pull emacski/tensorflow-serving:latest
- docker run -p 8501:8501 --mount type=bind,source=`pwd`/serving_dir/tip_hyperparam_model,target=/models/tip_hyperparam_model -e MODEL_NAME=tip_hyperparam_model -t emacski/tensorflow-serving:latest &
- curl -d '{"instances": [{"passenger_count":1, "trip_distance":12.2, "PULocationID":"193", "DOLocationID":"264", "payment_type":"2","fare_amount":20.4,"tolls_amount":0.0}]}' -X POST http://localhost:8501/v1/models/tip_hyperparam_model:predict
- http://localhost:8501/v1/models/tip_hyperparam_model