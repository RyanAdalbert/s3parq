# this script takes a generic formatted text file and outputs SQL values to be inserted into the transformation_variables table of the config DB

# by default, we use ~ as a delimiter as it shouldn't be used in variable naming/defining
# HEAD: pl_name~actor
# REST OF FILE: tv_name~tv_val~tt_name
# make sure your last line of data ends with a newline

import os

delimiter = '~'
filename = "var_vals.txt"
outfile = "out_vals.txt"

output = ""
with open(filename, "r") as f:
	head = f.readline()
	head = head[:-1]
	pos = head.find(delimiter)
	pl = head[:pos]
	actor = head[pos+1:]
	for line in f:
		line = line[:-1]
		first = line.find(delimiter)
		last = line.rfind(delimiter)
		name = line[:first]
		val = line[first+1:last]
		tt = line[last+1:]
		print(name, val, tt, '\n')

		sql = ( 
			f'(\'{name}\',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states '
		 	f'WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = \'{pl}\')) AND id = (SELECT id FROM transformations ' 
		 	f'WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv '
		 	f'ON t.id = tv.transformation_id WHERE tv.name = \'{name}\' ORDER BY t.id)) AND id IN (SELECT t.id from '
		 	f'transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE '
		 	f'tt.name = \'{tt}\')))ORDER BY id LIMIT 1), \'{val}\', \'{actor}\'),\n'
		 )

		output += sql

output = output[:-2] + ";"
out = open(outfile, "w+")
out.write(output)
out.close()