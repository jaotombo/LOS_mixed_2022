# Queries

## all_data_raw

Steps to get all_data_raw.csv

- run all_data_raw.sql in pgadmin to create a materialized view of most of the data (see below). Due to performance issues, I had to split the icd9 requests from the rest.
- run all_data_raw.ipynb

all_data_raw.csv contains 1156796 rows × 67 columns. No rows have been removed. Duplicates and dead patients are still there.


columns extracted from all_data_raw.sql:
	hadm_id,
	subject_id,
	admittime,
	dischtime,
	deathtime,
	ethnicity,
	admission_type,
	admission_location,
	insurance,
	religion,
	marital_status,
	discharge_location,
	costcenter,
	cpt_code,
	first_careunit,
	last_careunit,
	first_wardid,
	last_wardid,
	icu_los,
	prev_service,
	curr_service,
	gender,
	age,
	dob,
	urea_n_min,
	urea_n_max,
	urea_n_mean,
	platelets_min,
	platelets_max,
	platelets_mean,
	magnesium_max,
	albumin_min,
	calcium_min,
	resprate_min,
	resprate_max,
	resprate_mean,
	glucose_min,
	glucose_max,
	glucose_mean,
	hr_min,
	hr_max,
	hr_mean,
	sysbp_min,
	sysbp_max,
	sysbp_mean,
	diasbp_min,
	diasbp_max,
	diasbp_mean,
	temp_min,
	temp_max,
	temp_mean,
	sapsii,
	sofa,
	urine_min,
	urine_mean,
	urine_max,
	patientweight

Columns computed with all_data_raw.ipynb:
	icd9_code
	proc_icd9
	diag_icd9
	age_cat
	THS_cat
	prev_adm
	dest_discharge
	emergency_dpt
	icd_chapter
	origin_patient

## note_filter

To get the discharge notes and process them, run the note_filter.sql - then run the notebook 2_data_preparation.ipynb.