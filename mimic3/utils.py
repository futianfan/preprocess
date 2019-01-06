from datetime import datetime


minimum_admission_to_throw = 2
today = datetime.strptime('2125-01-01', '%Y-%m-%d')
separate_symbol_in_visit = ' '
separate_symbol_between_visit = ','
separate_symbol = '\t'


def convert_to_icd9(dx_str):
	if dx_str.startswith('E'):
		if len(dx_str) > 4: return dx_str[:4] + '.' + dx_str[4:]
		else: return dx_str
	else:
		if len(dx_str) > 3: return dx_str[:3] + '.' + dx_str[3:]
		else: return dx_str



def convert_to_3digit_icd9(dx_str):
	if dx_str.startswith('E'):
		if len(dx_str) > 4: return dx_str[:4]
		else: return dx_str
	else:
		if len(dx_str) > 3: return dx_str[:3]
		else: return dx_str

'''
if __name__ == "__main__":
	lst = ['E9352', '40391', '5781', 'V290', 'E915']
	out_lst = list(map(convert_to_icd9, lst))
	assert out_lst == ['E935.2', '403.91', '578.1', 'V29.0', 'E915']
	out_lst2 = list(map(convert_to_3digit_icd9, lst))
	assert out_lst2 == ['E935', '403', '578', 'V29', 'E915']

'''


### patient_id map to mortality label 
def patientid_map_label(patient_files):
	lines = open(patient_files, 'r').readlines()
	lines = lines[1:]
	f1 = lambda x: 1 if len(x) > 0 else 0
	patient_id_2_label = {
					int(line.strip().split(',')[1]): f1(line.strip().split(',')[5])
					 for line in lines
					 }
	return patient_id_2_label
	### key: SUBJECT_ID
	### value 1 / 0 


def patientid_map_admissionid_and_time(admission_file):
	from collections import defaultdict
	patient_id_2_admission = defaultdict(lambda: [])
	admission_id_2_time = {}
	lines = open(admission_file, 'r').readlines()
	lines = lines[1:]
	for line in lines:
		tokens = line.strip().split(',')
		patient_id = int(tokens[1])
		admission_id = int(tokens[2])
		admission_time = datetime.strptime(tokens[3], '%Y-%m-%d %H:%M:%S')
		admission_id_2_time[admission_id] = admission_time
		patient_id_2_admission[patient_id] += [admission_id]

	return patient_id_2_admission, admission_id_2_time


def admissionid_map_icdcode(diagnosis_file):
	from collections import defaultdict
	admission_id_2_icd = defaultdict(lambda: [])
	admission_id_2_icd_3digit = defaultdict(lambda: [])
	lines = open(diagnosis_file, 'r').readlines()
	lines = lines[1:]
	for line in lines:
		tokens = line.strip().split(',')
		admission_id = int(tokens[2])
		icd9_code = 'D_' + convert_to_icd9(tokens[4][1:-1])
		icd9_3_digits_code = 'D_' + convert_to_3digit_icd9(tokens[4][1:-1])

		admission_id_2_icd[admission_id] += [icd9_code]
		admission_id_2_icd_3digit[admission_id] += [icd9_3_digits_code]
	return admission_id_2_icd, admission_id_2_icd_3digit



def patientid_map_icdcode_and_time(
				patient_id_2_admission, 
				admission_id_2_time, 
				admission_id_2_icd, 
				admission_id_2_icd_3digit):
	from collections import defaultdict
	patient_id_2_icd_and_time = defaultdict(lambda: [])
	patient_id_2_icd3digit_and_time = defaultdict(lambda: [])

	for patient_id, admission_id_lst in patient_id_2_admission.items():
		if len(admission_id_lst) < minimum_admission_to_throw:   
			continue

		patient_id_2_icd_and_time[patient_id] = sorted([
												(admission_id_2_time[admission_id], admission_id_2_icd[admission_id]) 
												for admission_id in admission_id_lst
											 ])

		patient_id_2_icd3digit_and_time[patient_id] = sorted([
														(admission_id_2_time[admission_id], admission_id_2_icd_3digit[admission_id]) 
														for admission_id in admission_id_lst
													])

	return patient_id_2_icd_and_time, patient_id_2_icd3digit_and_time





def generate_whole_list(patient_id_2_icd_and_time, patient_id_2_icd3digit_and_time, patient_id_2_label):
	patient_id_lst = []
	time_list = []
	seq_lst = []
	label_lst = []
	seq3digit_lst = []

	for patient_id, visits in patient_id_2_icd_and_time.items():
		patient_id_lst.append(patient_id)
		label_lst.append(patient_id_2_label[patient_id])
		seq = [i[1] for i in visits]
		times = [i[0] for i in visits]
		seq_lst.append(seq)
		time_list.append(times)

	for patient_id, visits in patient_id_2_icd3digit_and_time.items():
		seq = [i[1] for i in visits]
		seq3digit_lst.append(seq)

	return patient_id_lst, time_list, seq_lst, seq3digit_lst, label_lst


def update_seq(seqs):
	"""
		old seq are composed of ICD9 code.
		new seq are composed of index, from 0, 1, 2, ...
	"""
	from collections import defaultdict
	icdcode2idx = defaultdict(lambda: len(icdcode2idx))
	new_seqs = [[[icdcode2idx[j] for j in admis]  for admis in seq] for seq in seqs]
	print('number of code is {}'.format(len(icdcode2idx)))
	#print(new_seqs)
	return new_seqs


def date_to_time(time_list):
	return [[(today - date).days for date in j] for j in time_list]



def lst_to_string(seq_idx_lst):

	f1 = lambda x: separate_symbol_in_visit.join(list(map(lambda y:str(y), x)))
	"""
		f1: [1,2,3] => '1 2 3'
	"""
	f2 = lambda x: separate_symbol_between_visit.join(list(map(f1, x)))
	"""
		[[1,2,3], [2,3,4]] =>  '1 2 3,2 3 4'
		
	"""
	return list(map(f2, seq_idx_lst))

'''
if __name__ == "__main__":
	a = [[[1,2,3], [2,3,4]], [[1,2,3], [2,3,4]]]
	print(lst_to_string(a))
'''



'''

    print('Making additional modifications to the data')
    #Compute time to today as to_event column
    today = datetime.strptime('2025-01-01', '%Y-%m-%d')
    to_event = [[(today-date).days for date in patient] for patient in dates]
    #Compute time of the day when the person was admitted as the numeric column of size 1
    numerics = [[[date.hour * 60 + date.minute - 720] for date in patient] for patient in dates]
    #Add this feature to dictionary but leave 1 index empty for PADDING
    types['Time of visit'] = len(types)+1
    types_3digit['Time of visit'] = len(types_3digit)+1
    #Compute sorting indicies
    sort_indicies = np.argsort(list(map(len, to_event)))
    #Create the dataframes of data and sort them according to number of visits per patient
    all_data = pd.DataFrame(data={'codes': new_seqs,
                                  'to_event': to_event,
                                  'numerics': numerics}
                           ,columns=['codes', 'to_event', 'numerics'])\
                          .iloc[sort_indicies].reset_index()
    all_data_3digit = pd.DataFrame(data={'codes': new_seqs_3digit,
                                         'to_event': to_event,
                                         'numerics': numerics}
                                  ,columns=['codes', 'to_event', 'numerics'])\
                                 .iloc[sort_indicies].reset_index()
    all_targets = pd.DataFrame(data={'target': morts}
                               ,columns=['target'])\
                              .iloc[sort_indicies].reset_index()


'''











