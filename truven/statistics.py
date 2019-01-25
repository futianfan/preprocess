outputfile = 'result/output'

lines = open(outputfile, 'r').readlines()
visit_num = list(map(lambda x: len(x.split(';')), lines))
print('average visit number is {}'.format(sum(visit_num) / len(visit_num)))

f = lambda x: len(' '.join(x.split(';')).split())
num_clinical_variable_for_patient = list(map(f, lines))
print('average visit number is {}'.\
	format(sum(num_clinical_variable_for_patient) / len(num_clinical_variable_for_patient)))


