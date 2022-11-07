# SQL Queries

We imported the MIMIC-III dataset on a PostgreSQL 14 server. We then run some basic queries found in https://github.com/MIT-LCP/mimic-code/blob/main/mimic-iii/ to get the SAPSII and SOFA tables. FInally we ran the all_data.sql to get the actual final tabular dataset.

The correct order to run is the following:

0. postgres-functions
1. blood_gas_first_day
2. blood_gas_first_day_arterial
3. ventilation_classification
4. ventilation_durations
5. gcs_first_day
6. urine_output_first_day
7. labs_first_day
8. echo_data
9. sapsii
10. sofa
11. all_data