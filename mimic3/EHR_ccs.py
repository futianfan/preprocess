import sys
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from datetime import datetime
import os 

'''
from utils import patientid_map_label, patientid_map_admissionid_and_time, \
				admissionid_map_icdcode, patientid_map_icdcode_and_time, \
				generate_whole_list, update_seq, date_to_time, \
				lst_to_string, separate_symbol, \
				separate_symbol_between_visit
'''

from utils import * 
###### input & hyperparameter

raw_data_folder = 'data'
out_data_folder = 'result'
test_proportion = 0.2


admission_file = os.path.join(raw_data_folder, 'ADMISSIONS.csv')
diagnosis_file = os.path.join(raw_data_folder, 'DIAGNOSES_ICD.csv')
patients_file = os.path.join(raw_data_folder, 'PATIENTS.csv')
output_file = os.path.join(out_data_folder, 'MimicCcs')
#output3digit_file = os.path.join(out_data_folder, 'output3digit')


if __name__ == '__main__':
	## patient_id => label	
	patient_id_2_label = patientid_map_label(patients_file)

	## patient_id => admission_id & time
	patient_id_2_admission, admission_id_2_time = patientid_map_admissionid_and_time(admission_file)

	## patient_id => icd-code & icd-code-3digits
	admission_id_2_ccscode  = admissionid_map_ccs(diagnosis_file)

	## patient_id => icd-code and time & icd-code-3digits and time 
	patient_id_2_ccs_and_time = patientid_map_ccscode_and_time(patient_id_2_admission, 
																admission_id_2_time, 
																admission_id_2_ccscode
															)


	patient_id_lst, time_list, seq_lst, label_lst = generate_whole_list_ccs(patient_id_2_ccs_and_time,\
																						 patient_id_2_label)
	seq_lst = lst_to_string(seq_lst)

	##  seq_idx_lst: [patient1, patient2, xxxxx]
	##  patient1: [visit1, visit2, xxxx]
	##  visit1: [1,5,3,xxxx] admission_idx for the visit 

	#seq_idx_lst = update_seq(seq_lst)
	#seq3digit_idx_lst = update_seq(seq3digit_lst) 
	"""
		old seq are composed of ICD9 code.
		new seq are composed of index, from 0, 1, 2, ...
	"""
	
	time_list = date_to_time(time_list)
	time_list = [separate_symbol_between_visit.join([str(i) for i in time]) for time in time_list]

	#seq_idx_lst = lst_to_string(seq_idx_lst)
	#seq3digit_idx_lst = lst_to_string(seq3digit_idx_lst)


	lines = [ str(patient_id) + separate_symbol \
			  + timestamp + separate_symbol \
			  + seq + separate_symbol \
			  + str(label) + '\n'
				for patient_id, timestamp, seq, label 
				in zip(patient_id_lst, time_list, seq_lst, label_lst)]



	train_line, test_line = train_test_split(lines, test_size = test_proportion)
	with open(output_file + 'Train', 'w') as fout:
		for line in train_line:
			fout.write(line)

	with open(output_file + 'Test', 'w') as fout:
		for line in test_line:
			fout.write(line)
	


















