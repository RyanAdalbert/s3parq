# SQL generation helper scripts

## Why?
Until we have a full-fledged frontend, the configuration DB can only be seeded using manual SQL commits. As some transformations contain hundreds of variables, it is unreasonable to expect to generate SQL for this process manually. Enter [var\_struct\_formatter](../script/var_struct_formatter.py) and [var\_val\_formatter](../script/var_val_formatter.py). 

### var\_struct\_formatter
The SQL excerpt
`
INSERT INTO transformation_templates (name, variable_structures, pipeline_state_type_id, last_actor) 
    VALUES
       ('initial_ingest', 
        '{"delimiter":{"datatype": "string", "description": "the input file delimiter"},"skip_rows":{"datatype":"int","description":"the number of rows to skip at the top of the file"},"encoding":{"datatype":"string","description":"the encoding of the input file"},"input_file_prefix":{"datatype":"string","description":"the prefix of the selected input files"}}', 
        (SELECT id FROM pipeline_state_types WHERE name = 'ingest'),
        'njb@integrichain.com');
`
adds a transformation template with a defined variable schema. var\_struct\_formatter takes a path `filename` (check the script variables) containing a list of variables in the format `variable_name~variable_type~variable_description` and outputs a file to path `outfile`. Make sure your input file ends with a newline!!! The output file contains a list of `variable_structures` in the format

`'{"variable_name":{"datatype": "variable_type", "description": "variable_description"},"variable2_name":{"datatype":"variable2_type","description":"variable2_description"}}'`

### var\_val\_formatter
Core loads the pipeline variable values through the transformation\_variables table. This SQL defines a set of variable values for the above variable_structure:
`
INSERT INTO transformation_variables (name, transformation_id, value, last_actor)
    VALUES
        ('delimiter',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'delimiter' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'initial_ingest')))ORDER BY id LIMIT 1), '|', 'njb@integrichain.com'),
        ('skip_rows',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'skip_rows' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'initial_ingest')))ORDER BY id LIMIT 1), '0', 'njb@integrichain.com'),
        ('encoding',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'encoding' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'initial_ingest')))ORDER BY id LIMIT 1), 'iso8859', 'njb@integrichain.com'),
        ('input_file_prefix',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_file_prefix' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'initial_ingest')))ORDER BY id LIMIT 1), 'upload.sha_dry_run_test_raw_fetch.INTEGRICHAIN_SUN_ACCREDO_STATUSDISPENSE', 'njb@integrichain.com');
`

Using the pipeline & transformation names, this logic returns a transformation\_id corresponding to a transform in the pipeline without transformation variables currently assigned. This is useful for transformations using the same template which run multiple times using different variable assignments, such as initial\_ingest. var\_val\_formatter generates a list of these insert statements from a path `filename` and outputs a file to path `outfile`. Make sure your input file ends with a newline!!! For example, an input file:
`
pipeline_name~actor@integrichain.com
var_name~var_val~transform_name
var2_name~var2_val~transform_name
var3_name~var3_val~transform2_name
`

would generate this `outfile`:
`
INSERT INTO transformation_variables (name, transformation_id, value, last_actor)
    VALUES
        ('var_name',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'pipeline_name')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'var_name' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'transform_name')))ORDER BY id LIMIT 1), 'var_val', 'actor@integrichain.com'),
        ('var2_name',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'pipeline_name')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'var2_name' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'transform_name')))ORDER BY id LIMIT 1), 'var2_val', 'actor@integrichain.com'),
        ('var3_name',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'pipeline_name')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'var3_name' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'transform2_name')))ORDER BY id LIMIT 1), 'var3_val', 'actor@integrichain.com');
`
var\_val\_formatter currently inserts all values as strings, so be sure to adjust values for int/bool variables.