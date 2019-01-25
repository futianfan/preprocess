file = 'data/AppendixASingleDX.txt'
codemapfile = 'result/ccs_idx2text'
lines = open(file, 'r').readlines()
lines = lines[4:]
from collections import defaultdict

ccs2idx = defaultdict(lambda:len(ccs2idx))
idx2text = dict()
idx2icdcode = defaultdict(lambda:[])
icdcode2idx = dict()


for line in lines:
	if line[0].isdigit():
		ccs = line.split()[0]
		idx = ccs2idx[ccs]
		text = ' '.join(line.split()[1:])
		idx2text[idx] = text 
		continue 

	if line.strip() == '':
		continue

	line = line.strip()
	icdcode = line.split()
	idx2icdcode[idx].extend(icdcode)	

for idx in idx2icdcode:
	for icdcode in idx2icdcode[idx]:
		icdcode2idx[icdcode] = idx 

with open(codemapfile, 'w') as fout:
	for i in idx2text:
		fout.write(str(i) + '\t' + idx2text[i] + '\n')

