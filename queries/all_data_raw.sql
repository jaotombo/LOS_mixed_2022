-- View: mimiciii.all_data3

-- DROP MATERIALIZED VIEW IF EXISTS mimiciii.all_data3;

CREATE MATERIALIZED VIEW IF NOT EXISTS mimiciii.all_data3
TABLESPACE pg_default
AS
 WITH lab_aggs AS (
         SELECT le.subject_id,
            le.hadm_id,
            min(
                CASE
                    WHEN le.itemid = 51006 THEN le.valuenum
                    ELSE NULL::double precision
                END) AS urea_n_min,
            max(
                CASE
                    WHEN le.itemid = 51006 THEN le.valuenum
                    ELSE NULL::double precision
                END) AS urea_n_max,
            avg(
                CASE
                    WHEN le.itemid = 51006 THEN le.valuenum
                    ELSE NULL::double precision
                END) AS urea_n_mean,
            min(
                CASE
                    WHEN le.itemid = 51265 THEN le.valuenum
                    ELSE NULL::double precision
                END) AS platelets_min,
            max(
                CASE
                    WHEN le.itemid = 51265 THEN le.valuenum
                    ELSE NULL::double precision
                END) AS platelets_max,
            avg(
                CASE
                    WHEN le.itemid = 51265 THEN le.valuenum
                    ELSE NULL::double precision
                END) AS platelets_mean,
            max(
                CASE
                    WHEN le.itemid = 50960 THEN le.valuenum
                    ELSE NULL::double precision
                END) AS magnesium_max,
            min(
                CASE
                    WHEN le.itemid = 50862 THEN le.valuenum
                    ELSE NULL::double precision
                END) AS albumin_min,
            min(
                CASE
                    WHEN le.itemid = 50893 THEN le.valuenum
                    ELSE NULL::double precision
                END) AS calcium_min
           FROM mimiciii.labevents le
          WHERE le.hadm_id IS NOT NULL
          GROUP BY le.subject_id, le.hadm_id
          ORDER BY le.subject_id, le.hadm_id
        ), chartevent_aggs AS (
         SELECT chartevents.hadm_id,
            min(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[615, 618, 220210, 224690])) AND chartevents.valuenum > 0::double precision AND chartevents.valuenum < 70::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END) AS resprate_min,
            max(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[615, 618, 220210, 224690])) AND chartevents.valuenum > 0::double precision AND chartevents.valuenum < 70::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END) AS resprate_max,
            avg(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[615, 618, 220210, 224690])) AND chartevents.valuenum > 0::double precision AND chartevents.valuenum < 70::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END) AS resprate_mean,
            min(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[807, 811, 1529, 3745, 3744, 225664, 220621, 226537])) AND chartevents.valuenum > 0::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END) AS glucose_min,
            max(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[807, 811, 1529, 3745, 3744, 225664, 220621, 226537])) AND chartevents.valuenum > 0::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END) AS glucose_max,
            avg(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[807, 811, 1529, 3745, 3744, 225664, 220621, 226537])) AND chartevents.valuenum > 0::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END) AS glucose_mean,
            min(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[211, 220045])) AND chartevents.valuenum > 0::double precision AND chartevents.valuenum < 300::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END) AS hr_min,
            max(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[211, 220045])) AND chartevents.valuenum > 0::double precision AND chartevents.valuenum < 300::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END) AS hr_max,
            round(avg(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[211, 220045])) AND chartevents.valuenum > 0::double precision AND chartevents.valuenum < 300::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END)::numeric, 2) AS hr_mean,
            min(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[51, 442, 455, 6701, 220179, 220050])) AND chartevents.valuenum > 0::double precision AND chartevents.valuenum < 400::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END) AS sysbp_min,
            max(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[51, 442, 455, 6701, 220179, 220050])) AND chartevents.valuenum > 0::double precision AND chartevents.valuenum < 400::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END) AS sysbp_max,
            round(avg(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[51, 442, 455, 6701, 220179, 220050])) AND chartevents.valuenum > 0::double precision AND chartevents.valuenum < 400::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END)::numeric, 2) AS sysbp_mean,
            min(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[8368, 8440, 8441, 8555, 220180, 220051])) AND chartevents.valuenum > 0::double precision AND chartevents.valuenum < 300::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END) AS diasbp_min,
            max(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[8368, 8440, 8441, 8555, 220180, 220051])) AND chartevents.valuenum > 0::double precision AND chartevents.valuenum < 300::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END) AS diasbp_max,
            round(avg(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[8368, 8440, 8441, 8555, 220180, 220051])) AND chartevents.valuenum > 0::double precision AND chartevents.valuenum < 300::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END)::numeric, 2) AS diasbp_mean,
            min(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[223761, 678])) AND chartevents.valuenum > 70::double precision AND chartevents.valuenum < 120::double precision THEN (chartevents.valuenum - 32::double precision) / 1.8::double precision
                    WHEN (chartevents.itemid = ANY (ARRAY[223762, 676])) AND chartevents.valuenum > 10::double precision AND chartevents.valuenum < 50::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END) AS temp_min,
            max(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[223761, 678])) AND chartevents.valuenum > 70::double precision AND chartevents.valuenum < 120::double precision THEN (chartevents.valuenum - 32::double precision) / 1.8::double precision
                    WHEN (chartevents.itemid = ANY (ARRAY[223762, 676])) AND chartevents.valuenum > 10::double precision AND chartevents.valuenum < 50::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END) AS temp_max,
            round(avg(
                CASE
                    WHEN (chartevents.itemid = ANY (ARRAY[223761, 678])) AND chartevents.valuenum > 70::double precision AND chartevents.valuenum < 120::double precision THEN (chartevents.valuenum - 32::double precision) / 1.8::double precision
                    WHEN (chartevents.itemid = ANY (ARRAY[223762, 676])) AND chartevents.valuenum > 10::double precision AND chartevents.valuenum < 50::double precision THEN chartevents.valuenum
                    ELSE NULL::double precision
                END)::numeric, 2) AS temp_mean
           FROM mimiciii.chartevents
          WHERE (chartevents.itemid = ANY (ARRAY[615, 618, 220210, 224690, 807, 811, 1529, 3745, 3744, 225664, 220621, 226537, 211, 220045, 51, 442, 455, 6701, 220179, 220050, 8368, 8440, 8441, 8555, 220180, 220051, 223761, 678, 223762, 676])) AND chartevents.hadm_id IS NOT NULL
          GROUP BY chartevents.hadm_id
        ), output_agg AS (
         SELECT outputevents.hadm_id,
            min(outputevents.value) AS urine_min,
            max(outputevents.value) AS urine_max,
            round(avg(outputevents.value)::numeric) AS urine_mean
           FROM mimiciii.outputevents
          WHERE (outputevents.itemid = ANY (ARRAY[40055, 226559])) AND outputevents.hadm_id IS NOT NULL
          GROUP BY outputevents.hadm_id
        ), ce0 AS (
         SELECT c.icustay_id,
            c.subject_id,
                CASE
                    WHEN c.itemid = ANY (ARRAY[920, 1394, 4187, 3486]) THEN c.valuenum * 2.54::double precision
                    ELSE c.valuenum
                END AS height
           FROM mimiciii.chartevents c
             JOIN mimiciii.icustays ie_1 ON c.icustay_id = ie_1.icustay_id AND c.charttime <= mimiciii.datetime_add(ie_1.intime, '1 day'::interval) AND c.charttime > mimiciii.datetime_sub(ie_1.intime, '1 day'::interval)
          WHERE c.valuenum IS NOT NULL AND (c.itemid = ANY (ARRAY[226730, 920, 1394, 4187, 3486, 3485, 4188])) AND c.valuenum <> 0::double precision AND (c.error IS NULL OR c.error = 0)
        ), ce AS (
         SELECT ce0.icustay_id,
            ce0.subject_id,
            avg(ce0.height) AS height_chart
           FROM ce0
          WHERE ce0.height > 100::double precision
          GROUP BY ce0.icustay_id, ce0.subject_id
        ), echo AS (
         SELECT ec.subject_id,
            2.54 * avg(ec.height) AS height_echo
           FROM mimiciii.echo_data ec
             JOIN mimiciii.icustays ie_1 ON ec.subject_id = ie_1.subject_id AND ec.charttime < mimiciii.datetime_add(ie_1.intime, '1 day'::interval)
          WHERE ec.height IS NOT NULL AND (ec.height * 2.54) > 100::numeric
          GROUP BY ec.subject_id
        ), height_chart AS (
         SELECT ie_1.icustay_id,
            ie_1.subject_id,
            COALESCE(ce.height_chart, ec.height_echo::double precision) AS height,
            ce.height_chart,
            ec.height_echo
           FROM mimiciii.icustays ie_1
             JOIN mimiciii.patients pat ON ie_1.subject_id = pat.subject_id AND ie_1.intime > mimiciii.datetime_add(pat.dob, '1 year'::interval)
             LEFT JOIN ce ON ie_1.subject_id = ce.subject_id
             LEFT JOIN echo ec ON ie_1.subject_id = ec.subject_id
        ), diag_icd AS (
         SELECT diagnoses_icd.hadm_id,
            diagnoses_icd.subject_id,
            string_agg(diagnoses_icd.icd9_code::text, ','::text) AS diag_icd9
           FROM mimiciii.diagnoses_icd
          GROUP BY diagnoses_icd.hadm_id, diagnoses_icd.subject_id
          ORDER BY diagnoses_icd.subject_id
        ), proc_icd AS (
         SELECT procedures_icd.hadm_id,
            procedures_icd.subject_id,
            string_agg(procedures_icd.icd9_code::text, ','::text) AS proc_icd9
           FROM mimiciii.procedures_icd
          GROUP BY procedures_icd.hadm_id, procedures_icd.subject_id
          ORDER BY procedures_icd.subject_id
        ), weight AS (
         SELECT inputevents_mv.patientweight,
            inputevents_mv.hadm_id,
            inputevents_mv.subject_id
           FROM mimiciii.inputevents_mv
          GROUP BY inputevents_mv.subject_id, inputevents_mv.hadm_id, inputevents_mv.patientweight
        )
 SELECT la.hadm_id,
    la.subject_id,
    ad.admittime,
    ad.dischtime,
    ad.deathtime,
    ad.ethnicity,
    ad.admission_type,
    ad.admission_location,
    ad.insurance,
    ad.religion,
    ad.marital_status,
    ad.discharge_location,
    cptevents.costcenter,
    cptevents.cpt_cd AS cpt_code,
    ie.first_careunit,
    ie.last_careunit,
    ie.first_wardid,
    ie.last_wardid,
    ie.los AS icu_los,
    services.prev_service,
    services.curr_service,
    p.gender,
    EXTRACT(epoch FROM ad.admittime - p.dob) / 60.0 / 60.0 / 24.0 / 365.242 AS age,
    p.dob,
    la.urea_n_min,
    la.urea_n_max,
    la.urea_n_mean,
    la.platelets_min,
    la.platelets_max,
    la.platelets_mean,
    la.magnesium_max,
    la.albumin_min,
    la.calcium_min,
    ca.resprate_min,
    ca.resprate_max,
    ca.resprate_mean,
    ca.glucose_min,
    ca.glucose_max,
    ca.glucose_mean,
    ca.hr_min,
    ca.hr_max,
    ca.hr_mean,
    ca.sysbp_min,
    ca.sysbp_max,
    ca.sysbp_mean,
    ca.diasbp_min,
    ca.diasbp_max,
    ca.diasbp_mean,
    ca.temp_min,
    ca.temp_max,
    ca.temp_mean,
    sapsii.sapsii,
    sofa.sofa,
    oa.urine_min,
    oa.urine_mean,
    oa.urine_max,
    weight.patientweight
   FROM lab_aggs la
     JOIN mimiciii.admissions ad ON la.hadm_id = ad.hadm_id
     JOIN mimiciii.cptevents ON la.hadm_id = cptevents.hadm_id
     JOIN mimiciii.icustays ie ON la.hadm_id = ie.hadm_id
     JOIN mimiciii.services ON la.hadm_id = services.hadm_id
     JOIN mimiciii.patients p ON la.subject_id = p.subject_id
     JOIN output_agg oa ON la.hadm_id = oa.hadm_id
     JOIN chartevent_aggs ca ON la.hadm_id = ca.hadm_id
     JOIN mimiciii.sapsii ON la.hadm_id = sapsii.hadm_id
     JOIN mimiciii.sofa ON la.hadm_id = sofa.hadm_id
     LEFT JOIN weight ON la.hadm_id = weight.hadm_id
  GROUP BY la.hadm_id, la.subject_id, ad.admittime, ad.dischtime, ad.deathtime, ad.ethnicity, ad.admission_type, ad.admission_location, ad.insurance, ad.religion, ad.marital_status, ad.discharge_location, cptevents.costcenter, cptevents.cpt_cd, ie.first_careunit, ie.last_careunit, ie.first_wardid, ie.last_wardid, ie.los, services.prev_service, services.curr_service, p.gender, (EXTRACT(epoch FROM ad.admittime - p.dob) / 60.0 / 60.0 / 24.0 / 365.242), p.dob, la.urea_n_min, la.urea_n_max, la.urea_n_mean, la.platelets_min, la.platelets_max, la.platelets_mean, la.magnesium_max, la.albumin_min, la.calcium_min, ca.resprate_min, ca.resprate_max, ca.resprate_mean, ca.glucose_min, ca.glucose_max, ca.glucose_mean, ca.hr_min, ca.hr_max, ca.hr_mean, ca.sysbp_min, ca.sysbp_max, ca.sysbp_mean, ca.diasbp_min, ca.diasbp_max, ca.diasbp_mean, ca.temp_min, ca.temp_max, ca.temp_mean, sapsii.sapsii, sofa.sofa, oa.urine_min, oa.urine_mean, oa.urine_max, weight.patientweight
  ORDER BY la.hadm_id, ad.admittime
WITH DATA;

ALTER TABLE IF EXISTS mimiciii.all_data3
    OWNER TO postgres;