import os
from datetime import datetime


filename = 'Mdcri113.csv'
data_folder = 'data'
separate_symbol = ','
filename = os.path.join(data_folder, filename)

adm_code_idx = list(range(35,50))



with open(filename, 'r') as fin:
	lines = fin.readlines()[1:]
	### remove the first line

	for j,line in enumerate(lines): 
		line = line.split(separate_symbol)
		if (line[3] == ''):
			continue
		enrol_id = line[3]
		month, days, year = [int(i) for i in line[6].split('/')]
		day = datetime(year, month, days)
		adm_code = [line[i] for i in adm_code_idx]
		adm_code = list(filter(None, adm_code))   ### filter out ''
		print(adm_code)














