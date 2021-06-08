import fileinput, re

start_comb_pat = re.compile(r'\[start_combation\]:(\d+)%(\d+)')
comb_list_pat = re.compile(r'\[\w+\]:(\d+)')
com_id_pat = re.compile(r'(\w+):(*)')

