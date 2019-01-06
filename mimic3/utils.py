from datetime import datetime


minimum_admission_to_throw = 5

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







    print('Converting strSeqs to intSeqs, and making types')
    types = {}
    new_seqs = []
    for patient in seqs:
        new_patient = []
        for visit in patient:
            new_visit = []
            for code in visit:
                if code in types:
                    new_visit.append(types[code])
                else:
                    types[code] = len(types)
                    new_visit.append(types[code])
            new_patient.append(new_visit)
        new_seqs.append(new_patient)

    print('Converting strSeqs to intSeqs, and making types for 3digit ICD9 code')
    types_3digit = {}
    new_seqs_3digit = []
    for patient in seqs_3digit:
        new_patient = []
        for visit in patient:
            new_visit = []
            for code in set(visit):
                if code in types_3digit:
                    new_visit.append(types_3digit[code])
                else:
                    types_3digit[code] = len(types_3digit)
                    new_visit.append(types_3digit[code])
            new_patient.append(new_visit)
        new_seqs_3digit.append(new_patient)














