from seeds import seedbot
import pytest, os

def _set_globals():
    seedbot.TT_NAME = "test-template"
    seedbot.TT_STATE = "master"
    seedbot.TT_VARIABLE_NAMES = ['foo', 'bar']
    seedbot.TT_VARIABLE_TYPES = ['str', 'int']
    seedbot.TT_VARIABLE_DESCRIPTIONS = ['dummy description for foo', 'dummy description for bar']
    seedbot.VARIABLE_COUNT = 2
    seedbot.ACTOR = 'act@integrichain.com'
    seedbot.TR_PIPELINE_NAMES = ['test-pl1', 'test-pl2', 'test-pl3']
    seedbot.TR_GRAPH_ORDERS = [2, 1, 3]
    seedbot.TV_VARIABLE_NAMES = [['foo', 'bar'], ['foo', 'bar'], ['foo', 'bar']]
    seedbot.TV_VARIABLE_VALUES = [['a', 22], ['xD', 100], ['wow', 22]]
    return

def test_generate_tt():
    _set_globals()
    expected = f"BEGIN;\n\tINSERT INTO transformation_templates\n\t\t(name, variable_structures, pipeline_state_type_id, last_actor)\n\tVALUES\n\t\t('{seedbot.TT_NAME}',\n\t\t'{{"
    expected += f'"{seedbot.TT_VARIABLE_NAMES[0]}":{{"datatype": "{seedbot.TT_VARIABLE_TYPES[0]}", "description": "{seedbot.TT_VARIABLE_DESCRIPTIONS[0]}"}},\n\t\t\t"{seedbot.TT_VARIABLE_NAMES[1]}":{{"datatype": "{seedbot.TT_VARIABLE_TYPES[1]}", "description": "{seedbot.TT_VARIABLE_DESCRIPTIONS[1]}"}}'
    expected += "}',"
    expected += f"\n\t\t(SELECT id FROM pipeline_state_types WHERE name = '{seedbot.TT_STATE}'),\n\t\t'{seedbot.ACTOR}');\nCOMMIT;"

    assert seedbot._generate_tt_sql() == expected

def test_generate_tr():
    _set_globals()
    expected = f"BEGIN;\n\tINSERT INTO transformations\n\t\t(transformation_template_id, pipeline_state_id, graph_order, last_actor)\n\tVALUES\n"
    for i in range(len(seedbot.TR_PIPELINE_NAMES)):
        expected += f"\t\t((SELECT id FROM transformation_templates WHERE name = '{seedbot.TT_NAME}'),\n\t\t(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = '{seedbot.TT_STATE}') AND pipeline_id = (SELECT id FROM pipelines WHERE name = '{seedbot.TR_PIPELINE_NAMES[i]}')),\n\t\t{seedbot.TR_GRAPH_ORDERS[i]},\n\t\t'{seedbot.ACTOR}'),\n"
    expected = expected[:-2] + ";\nCOMMIT;"

    assert seedbot._generate_tr_sql() == expected

def test_generate_tv():
    _set_globals()
    expected = f"BEGIN;\n\tINSERT INTO transformation_variables\n\t\t(name, transformation_id, value, last_actor)\n\tVALUES\n"
    for i in range(len(seedbot.TR_PIPELINE_NAMES)):
        variables = dict(zip(seedbot.TV_VARIABLE_NAMES[i], seedbot.TV_VARIABLE_VALUES[i]))
        for name, val in variables.items():
            expected += f"\t\t('{name}',\n\t\t(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = '{seedbot.TR_PIPELINE_NAMES[i]}')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = '{name}' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = '{seedbot.TT_NAME}')))ORDER BY id LIMIT 1),\n\t\t'{val}',\n\t\t'{seedbot.ACTOR}'),\n"
    expected = expected[:-2] + ";\nCOMMIT;"

    assert seedbot._generate_tv_sql() == expected