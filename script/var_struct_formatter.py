# this script takes a generic formatted text file and outputs JSON formatted for the variable_structures field for transformation templates

# by default, we use ~ as a delimiter as it shouldn't be used in variable naming/describing
# format of your input file should follow the syntax VAR_NAME~VAR_TYPE~DESCRIPTION
# ~DESCRIPTION is an optional field but strongly recommended
# make sure your last line of data ends with a newline

import os

delimiter = '~'
filename = "variables.txt"
outfile = "out_structs.txt"

output = "\'{"
with open(filename, "r") as f:
	for line in f:
		line = line[:-1]
		if line.count(delimiter) == 2:
			pos = line.rfind(delimiter)
			desc = line[pos+1:]
			line = line[:pos]
		else:
			desc = ""
		pos = line.find(delimiter)
		name = line[:pos]
		datatype = line[pos+1:]
		output += "\"" + name + "\":{\"datatype\": \"" + datatype + "\", \"description\": \"" + desc + "\"},"

output = output[:-1] + "}\'"
out = open(outfile, "w+")
out.write(output)
out.close()