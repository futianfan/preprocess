import os
from datetime import datetime
from utils import convert_to_3digit_icd9
from time import time 
from ccs import icdcode2idx


filename_lst = ['Mdcri113.csv', 'Mdcri133.csv', 'Mdcri123.csv', 'Mdcri142.csv']
filename = 'Mdcri113.csv'
file_output = 'output_ccs'
code2idx_file = 'code2idx_ccs'
data_folder = 'data'
result_folder = 'result'
separate_symbol = ','
filename = os.path.join(data_folder, filename)
file_output = os.path.join(result_folder, file_output)
code2idx_file = os.path.join(result_folder, code2idx_file)
adm_code_idx = list(range(35,50))

minimum_visit = 5 
maximum_visit = 20



time_bgn = time()
lines = []
for filename in filename_lst:
	fname = os.path.join(data_folder, filename)
	fin = open(fname, 'r')
	lines += fin.readlines()[1:]
	### remove the first line

def process(lines):
	adm_code_set = set()  ### the whole icd9 code
	patient_dict = dict()
	for j,line in enumerate(lines): 
		line = line.split(separate_symbol)
		if (line[3] == ''):
			continue

		### 1 enroll id == patient id
		enrol_id = line[3]
		if enrol_id not in patient_dict:
			patient_dict[enrol_id] = dict()

		### 2 date
		month, days, year = [int(i) for i in line[6].split('/')]
		day = datetime(year, month, days)

		### 3 admission code 
		adm_code = [line[i] for i in adm_code_idx]
		### filter out ''
		adm_code = list(filter(None, adm_code))   
		### CCS 
		convert_f = lambda x:icdcode2idx[x]
		adm_code = list(map(convert_f, adm_code)) 
		if len(adm_code) == 0: continue ### throw empty data 
		if day not in patient_dict[enrol_id]: 
			patient_dict[enrol_id][day] = adm_code
		else:
			patient_dict[enrol_id][day] += adm_code

		adm_code_set = adm_code_set.union(set(adm_code))  ### the whole icd9 code

	print('size of admission code is {}'.format(len(adm_code_set)))
	print('collapse {} seconds'.format(int(time() - time_bgn)))
	code2idx = {code:idx for idx,code in enumerate(list(adm_code_set))}
	idx2code = {idx:code for code,idx in code2idx.items()}
	f = lambda v:[code2idx[i] for i in v]
	### patient_dict  delete the key that has less than minimum_visit
	key_lst = list(patient_dict.keys())
	for k in key_lst:
		if len(patient_dict[k]) < minimum_visit:
			patient_dict.pop(k)

	new_patient_dict = dict()
	### sorted by datetime and choose at most maximum_visit 
	for keys in patient_dict:
		sorted_lst = sorted([(k,f(v)) for k,v in patient_dict[keys].items()])
		sorted_lst = sorted_lst[-maximum_visit:]
		new_patient_dict[keys] = sorted_lst
	print('collapse {} seconds'.format(int(time() - time_bgn)))

	fout = open(file_output, 'w')
	for keys in new_patient_dict:
		lst = new_patient_dict[keys]
		visits = [v for (k,v) in lst]
		string = ';'.join([' '.join([str(j) for j in i]) for i in visits])
		####  [[1,2], [3,4]] => '1 2;3 4'  list of list => string 
		fout.write(string + '\n')
	fout.close()




if __name__ == '__main__':
	process(lines)







