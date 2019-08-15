'''
┗┃・ ◡ ・┃┛ Hello World!

I am Seedbot. I generate SQL statements used to seed a transformation in the Core configuration database. I expect a CSV separated by DELIMITER saved to the path INPUT_PATH. Using that file, I write a file to the path specified as OUTPUT_PATH. By default, I'll look for an INPUT_PATH ./seedbot_input.csv separated by | and write to an OUTPUT_PATH ./{transform name}.sql. For example, a transform named patient_status_unblind would be saved to ./patient_status_unblind.sql.
'''

INPUT_PATH = ''
OUTPUT_PATH = ''
DELIMITER = ''

import csv, os

# constants pulled from the CSV injected into the resulting SQL
TT_NAME = ''
TT_STATE = ''
TT_VARIABLE_NAMES = []
TT_VARIABLE_TYPES = []
TT_VARIABLE_DESCRIPTIONS = []
TR_PIPELINE_NAMES = []
TR_GRAPH_ORDERS = []
TR_VARIABLE_NAMES = []
TR_VARIABLE_VALUES = []
ACTOR = ''
VARIABLE_COUNT = 0
VALID_STATES = ['raw', 'ingest', 'master', 'enhance', 'enrich', 'metrics', 'dimensional']
VALID_TYPES = ['str', 'string', 'char', 'varchar', 'text', 'datetime', 'date', 'int', 'integer', 'float', 'decimal', 'number', 'double', 'bool', 'boolean']

def _invalid_tt_head(tt_head)->bool:
    '''
    Returns true if and only if the transformation template header row of the input CSV doesn't follow the expected convention.
    This function sets the VARIABLE_COUNT from the number of variable name, type, and description "head" columns / 3. The number transformation template variable names, types, descriptions, and values must equal this VARIABLE_COUNT.
    '''
    if(len(tt_head) < 3 or len(tt_head) % 3 != 2):
        return True
    expected = ['tt.name', 'tt.state']
    tt_var = ['tt.varname', 'tt.vartype', 'tt.vardesc']
    VARIABLE_COUNT = (tt_head - 2) / 3
    for var in range(VARIABLE_COUNT): expected.extend(tt_var)
    
    return tt_head.sort() != expected.sort()

def _invalid_tr_head(tr_head)->bool:
    expected = ['tr.pipeline', 'tr.graphorder']
    tv_var = ['tv.name', 'tv.value']
    for var in range(VARIABLE_COUNT): expected.extend(tv_var)

    return tr_head.sort() != expected.sort()

def _parse_head(csv: csv.reader)->csv.reader:
    '''
    Parses the CSV through the final transformation header row and assigns corresponding constants to be used in the generated SQL statements.
    '''
    row = next(csv)
    if len(row) != 1 or row[0] != "email": 
        raise ValueError("Error: Invalid first row. Expected a single column with value 'email'.")

    row = next(csv)
    if len(row) != 1 or row[0].find('@') == -1:
        raise ValueError("Error: Invalid second row. Expected a single column with value set to your email address.")
    ACTOR = row[0]

    tt_head = next(csv)
    if _invalid_tt_head(tt_head):
        raise ValueError("Error: Invalid third row. Expected a header row for the transformation template.")

    row = next(csv) # tt values
    if len(row) != len(tt_head):
        raise ValueError("Error: Number of transform template field values (fourth row) does not equal number of transform template field names.")

    TT_NAME = row.pop(0)
    TT_STATE = row.pop(0)
    if TT_STATE not in VALID_STATES:
        raise ValueError(f"Error: Invalid tt.state. Expected one of {', '.join(VALID_STATES)}." )

    for var in range(VARIABLE_COUNT):
        TT_VARIABLE_NAMES.append(row.pop(0))
        var_type = row.pop(0)
        if var_type not in VALID_TYPES:
            raise ValueError(f"Error: Variable datatype {var_type} not supported in Core.")
        TT_VARIABLE_TYPES.append(var_type)
        TT_VARIABLE_DESCRIPTIONS.append(row.pop(0))
    
    row = next(csv)
    if _invalid_tr_head(row):
        raise ValueError("Error: Invalid fifth row. Expected a header row for the transformation & variables.")

    return csv

def _parse_variables(row: list)->None:
    var_names = []
    var_vals = []
    for var_num in range(VARIABLE_COUNT):
        var_name = row.pop(0)
        var_val = row.pop(0)
        assert var_name.lower() == TT_VARIABLE_NAMES[var_num].lower() # the tv name should match the tt var name
        var_names.append(var_name)
        var_vals.append(var_vals)
    TR_VARIABLE_NAMES.append(var_names)
    TR_VARIABLE_VALUES.append(var_vals)

def _parse_body(csv: csv.reader)->None:
    '''Parses the remainder of the CSV. These rows are all Transformation and TransformationVariable field values.'''
    row_num = 6 # this should be the first row of the body, i.e. the first tr/tv row (as opposed to tt)
    expected_len = 2 + (VARIABLE_COUNT * 2) # each row should have a pipeline name, graph order, and a name/value for each template variable
    for row in csv:
        if len(row) != expected_len:
            raise ValueError(f"Error at row {str(row_num)}. Expected {expected_len} columns but found {len(row)} columns.")
        TR_PIPELINE_NAMES.append(row[0])
        TR_GRAPH_ORDERS.append(int(row[1]))
        _parse_variables(row[2:])
        row_num += 1
    

with open(INPUT_PATH) as csv_file:
    csv = csv.reader(csv_file, delimiter=DELIMITER)
    _parse_body(_parse_head(csv))

