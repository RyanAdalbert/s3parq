'''
┗┃・ ◡ ・┃┛ Hello World!

I am Seedbot. I generate SQL statements used to seed a transformation in the Core
configuration database. I expect a CSV/TSV separated by DELIMITER saved to the path
INPUT_PATH. Using that file, I write a file to the path specified as OUTPUT_PATH.
By default, I'll look for an INPUT_PATH ./seedbot_input.tsv separated by \t and write
to an OUTPUT_PATH ./{transform name}.sql. For example, a transform named patient_status_unblind
would be saved to ./patient_status_unblind.sql.
'''

INPUT_PATH = None
OUTPUT_PATH = None
DELIMITER = '\t'

if INPUT_PATH is None: INPUT_PATH = 'seedbot_input.tsv'

import csv, os, sys
from core.logging import LoggerSingleton
logger = LoggerSingleton().logger

# constants pulled from the CSV injected into the resulting SQL
TT_NAME = ''
TT_STATE = ''
TT_VARIABLE_NAMES = []
TT_VARIABLE_TYPES = []
TT_VARIABLE_DESCRIPTIONS = []
TR_PIPELINE_NAMES = []
TR_GRAPH_ORDERS = []
TV_VARIABLE_NAMES = []
TV_VARIABLE_VALUES = []
ACTOR = ''
# other constants
VARIABLE_COUNT = 0
VALID_STATES = ['raw', 'ingest', 'master', 'enhance', 'enrich', 'metrics', 'dimensional']
VALID_TYPES = ['str', 'string', 'char', 'varchar', 'text', 'datetime', 'date', 'int', 'integer', 'float', 'decimal', 'number', 'double', 'bool', 'boolean']
NULL_VALUES = ('seedbot_null', 'seedbot-null', 'seedbot.null', 'seedbotnull')

def _strip_row(row: list)->list:
    return [x for x in row if x] # Seedbot only cares about cells in a row with data

def _invalid_tt_head(tt_head)->bool:
    '''
    Returns true if and only if the transformation template header row of the input CSV doesn't follow the expected convention.
    This function sets the VARIABLE_COUNT from the number of variable name, type, and description "head" columns / 3. The number transformation template variable names, types, descriptions, and values must equal this VARIABLE_COUNT.
    '''
    global VARIABLE_COUNT
    if(len(tt_head) < 3 or len(tt_head) % 3 != 2):
        return True
    expected = ['tt.name', 'tt.state']
    tt_var = ['tt.varname', 'tt.vartype', 'tt.vardesc']
    VARIABLE_COUNT = (len(tt_head) - 2) // 3
    for var in range(VARIABLE_COUNT): expected.extend(tt_var)
    
    return tt_head.sort() != expected.sort()

def _invalid_tr_head(tr_head)->bool:
    '''
    Returns true if and only if the transformation & variable header row of the input CSV doesn't follow our expected convention
    '''
    expected = ['tr.pipeline', 'tr.graphorder']
    tv_var = ['tv.name', 'tv.value']
    for var in range(VARIABLE_COUNT): expected.extend(tv_var)

    return tr_head.sort() != expected.sort()

def _parse_head(tsv: csv.reader)->csv.reader:
    global ACTOR, TT_NAME, TT_STATE, TT_VARIABLE_NAMES, TT_VARIABLE_TYPES, TT_VARIABLE_DESCRIPTIONS
    '''
    Parses the CSV through the final transformation header row and assigns corresponding constants to be used in the generated SQL statements.
    '''
    row = _strip_row(next(tsv))
    if len(row) != 1 or row[0] != "email": 
        raise ValueError("Error: Invalid first row. Expected a single column with value 'email'.")

    row = _strip_row(next(tsv))
    if len(row) != 1 or row[0].find('@') == -1:
        raise ValueError("Error: Invalid second row. Expected a single column with value set to your email address.")
    ACTOR = row[0]

    tt_head = _strip_row(next(tsv))
    if _invalid_tt_head(tt_head):
        raise ValueError("Error: Invalid third row. Expected a header row for the transformation template.")

    row = _strip_row(next(tsv)) # tt values
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
    
    row = _strip_row(next(tsv))
    if _invalid_tr_head(row):
        raise ValueError("Error: Invalid fifth row. Expected a header row for the transformation & variables.")

    return tsv

def _parse_variables(row: list)->None:
    global TT_VARIABLE_NAMES, TV_VARIABLE_NAMES, TV_VARIABLE_VALUES
    var_names = []
    var_vals = []
    for var_num in range(VARIABLE_COUNT):
        var_name = row.pop(0)
        var_val = row.pop(0)
        if var_name.lower() not in list(map(str.lower, TT_VARIABLE_NAMES)):
            raise ValueError(f"Error. Found variable {var_name} which is not in the transformation template for {TT_NAME}.")
        if var_val.lower() in NULL_VALUES: var_val = '' # variables with values in NULL_VALUES should be set to empty strings (null)
        var_names.append(var_name)
        var_vals.append(var_val)
    TV_VARIABLE_NAMES.append(var_names)
    TV_VARIABLE_VALUES.append(var_vals)

def _parse_body(tsv: csv.reader)->None:
    '''
    Parses the remainder of the CSV. These rows are all Transformation and TransformationVariable field values.
    '''
    row_num = 6 # this should be the first row of the body, i.e. the first tr/tv row of values, not headers (as opposed to tt)
    expected_len = 2 + (VARIABLE_COUNT * 2) # each row should have a pipeline name, graph order, and a name/value for each template variable
    for row in tsv:
        row = _strip_row(row)
        if len(row) != expected_len:
            raise ValueError(f"Error at row {str(row_num)}. Expected {expected_len} columns but found {len(row)} columns.")
        TR_PIPELINE_NAMES.append(row[0])
        TR_GRAPH_ORDERS.append(int(row[1]))
        _parse_variables(row[2:])
        row_num += 1
    if len(TR_PIPELINE_NAMES) == 0:
        raise ValueError(f"Error: No transformation rows found for template {TT_NAME}.")

def _tt_var_struct()->str:
    struct = "\t\t'{"
    for i in range(VARIABLE_COUNT):
        struct += f'"{TT_VARIABLE_NAMES[i]}":{{"datatype": "{TT_VARIABLE_TYPES[i]}", "description": "{TT_VARIABLE_DESCRIPTIONS[i]}"}},'
        struct += '\n\t\t\t'
    return struct[:-5] + "}'," # trims last comma and whitespace before returning end of struct

def _generate_tt_sql()->str:
    statement = f"BEGIN;\n\tINSERT INTO transformation_templates\n\t\t(name, variable_structures, pipeline_state_type_id, last_actor)\n\tVALUES\n\t\t('{TT_NAME}',\n"
    statement += _tt_var_struct() # JSON string handled in submodule
    statement += f"\n\t\t(SELECT id FROM pipeline_state_types WHERE name = '{TT_STATE}'),\n\t\t'{ACTOR}');\nCOMMIT;"
    return statement

def _generate_tr_sql()->str:
    statement = f"BEGIN;\n\tINSERT INTO transformations\n\t\t(transformation_template_id, pipeline_state_id, graph_order, last_actor)\n\tVALUES\n"
    for i in range(len(TR_PIPELINE_NAMES)):
        statement += f"\t\t((SELECT id FROM transformation_templates WHERE name = '{TT_NAME}'),\n\t\t(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = '{TT_STATE}') AND pipeline_id = (SELECT id FROM pipelines WHERE name = '{TR_PIPELINE_NAMES[i]}')),\n\t\t{TR_GRAPH_ORDERS[i]},\n\t\t'{ACTOR}'),\n"
    statement = statement[:-2] + ";\nCOMMIT;"
    return statement

def _generate_tv_sql()->str:
    statement = f"BEGIN;\n\tINSERT INTO transformation_variables\n\t\t(name, transformation_id, value, last_actor)\n\tVALUES\n"
    for i in range(len(TR_PIPELINE_NAMES)):
        variables = dict(zip(TV_VARIABLE_NAMES[i], TV_VARIABLE_VALUES[i]))
        for name, val in variables.items():
            statement += f"\t\t('{name}',\n\t\t(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = '{TR_PIPELINE_NAMES[i]}')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = '{name}' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = '{TT_NAME}')))ORDER BY id LIMIT 1),\n\t\t'{val}',\n\t\t'{ACTOR}'),\n"
    statement = statement[:-2] + ";\nCOMMIT;"
    return statement

def _set_output_path()->None:
    '''
    Sets the OUTPUT_PATH if it isn't specified at the top and validates that the output path is valid and doesn't already exist (unless we --force).
    '''
    global OUTPUT_PATH
    if OUTPUT_PATH is None:
        logger.info(f"No OUTPUT_PATH supplied. Using default ./{TT_NAME}.sql...")
        OUTPUT_PATH = f"{TT_NAME}.sql"
    if not str(OUTPUT_PATH).endswith('.sql'):
        raise ValueError(f"Error: Output path {OUTPUT_PATH} does not end in required .sql suffix.")
    if os.path.exists(OUTPUT_PATH):
        if len(sys.argv) != 2 or sys.argv[1].lower() not in ('f', '-f', '--force'):
            raise ValueError(f"Error: Output path {OUTPUT_PATH} already exists. Please call Seedbot with -f or --force if you wish to overwrite the existing file.")

    return

if __name__ == '__main__':
    with open(INPUT_PATH) as tsv_file:
        tsv = csv.reader(tsv_file, delimiter=DELIMITER)
        _parse_body(_parse_head(tsv)) # populates global configuration vars from tsv template
    logger.info(f"File {INPUT_PATH} successfully processed. Generating SQL for transform {TT_NAME}.")

    _set_output_path()

    contents = f"{_generate_tt_sql()}\n\n{_generate_tr_sql()}\n\n{_generate_tv_sql()}"
    logger.info(f"SQL successfully generated. Writing SQL to output file {OUTPUT_PATH}...")

    with open(OUTPUT_PATH, "w+") as output:
        output.write(contents) 
