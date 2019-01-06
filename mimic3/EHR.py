import sys
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from datetime import datetime
import os 


from utils import patientid_map_label, patientid_map_admissionid_and_time, \
				admissionid_map_icdcode, patientid_map_icdcode_and_time, \
				generate_whole_list

###### input & hyperparameter

raw_data_folder = 'data'
out_data_folder = 'result'

admission_file = os.path.join(raw_data_folder, 'ADMISSIONS.csv')
diagnosis_file = os.path.join(raw_data_folder, 'DIAGNOSES_ICD.csv')
patients_file = os.path.join(raw_data_folder, 'PATIENTS.csv')












if __name__ == '__main__':
	## patient_id => label	
	patient_id_2_label = patientid_map_label(patients_file)

	## patient_id => admission_id & time
	patient_id_2_admission, admission_id_2_time = patientid_map_admissionid_and_time(admission_file)

	## patient_id => icd-code & icd-code-3digits
	admission_id_2_icd, admission_id_2_icd_3digit = admissionid_map_icdcode(diagnosis_file)

	## patient_id => icd-code and time & icd-code-3digits and time 
	patient_id_2_icd_and_time, patient_id_2_icd3digit_and_time = patientid_map_icdcode_and_time(patient_id_2_admission, 
																								admission_id_2_time, 
																								admission_id_2_icd, 
																								admission_id_2_icd_3digit)


	patient_id_lst, time_list, seq_lst, seq3digit_lst, label_lst = generate_whole_list(patient_id_2_icd_and_time,\
																						 patient_id_2_icd3digit_and_time, \
																						 patient_id_2_label)










