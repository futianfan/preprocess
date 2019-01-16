

def convert_to_3digit_icd9(dx_str):
	if dx_str.startswith('E'):
		if len(dx_str) > 4: return dx_str[:4]
		else: return dx_str
	else:
		if len(dx_str) > 3: return dx_str[:3]
		else: return dx_str


