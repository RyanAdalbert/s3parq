import pytest
from core.contract import Contract

def test_set_env_valid():
    contract = Contract()
    contract.set_env('dev')
    assert contract.env == 'ichain-development', 'failed to set dev environment'

def test_set_env_invalid():
    contract = Contract()

    with pytest.raises(ValueError):
        contract.set_env('Merck')

def test_get_s3_path_not_empty():
    contract = Contract()
    with pytest.raises(ValueError):
                        contract.get_s3_path()


@pytest.fixture
def _contract():
    contract = Contract()
    contract.set_branch('master')
    contract.set_env('dev')
    contract.set_parent('Merck')
    contract.set_child('Wonder_Drug')
    contract.set_state('Ingest')
    contract.set_dataset('valid_dataset')       
    return contract


def test_dataset_only(_contract):
    contract = _contract
    path = contract.get_s3_path()

    assert path == 's3://ichain-development/Master/Merck/Wonder_drug/Ingest/valid_dataset/', 'path was incorrectly built.'

def test_with_partitions(_contract):
    contract = _contract
    contract.set_partitions(['partition_1','partition_2'])
    path = contract.get_s3_path()
    assert path == 's3://ichain-development/Master/Merck/Wonder_drug/Ingest/valid_dataset/partition_1/partition_2/', 'path was incorrectly built with partitions.'

'''
    ## with file_name
    contract.set_file_name('29980385023509.parquet')
    path = contract.get_s3_path()
    assert    path, 
                        's3://ichain-development/Master/Merck/Wonder_drug/Ingest/valid_dataset/partition_1/partition_2/29980385023509.parquet', 
                        'path was incorrectly built with partitions.'
                    )
    
    ## file_name, no partitions
    contract.partitions = [] # hack to jump around the 0 len guard

    path = contract.get_s3_path()
    assert    path, 
                        's3://ichain-development/Master/Merck/Wonder_drug/Ingest/valid_dataset/29980385023509.parquet', 
                        'path was incorrectly built without partitions and with file name.'
                    )

def test_quick_set(self):
    contract = Contract(branch = 'master',
                        env = 'dev',
                        parent = 'Merck',
                        child = 'Wonder_Drug',
                        state = 'Ingest',
                        dataset = 'valid_dataset')

    assert    contract.get_branch(), 'Master', 'failed to set branch') 
    assert    contract.get_env(), 'ichain-development', 'failed to set env') 
    assert    contract.get_parent(), 'Merck', 'failed to set parent') 
    assert    contract.get_child(), 'Wonder_drug', 'failed to set parent') 
    assert    contract.get_state(), 'Ingest', 'failed to set parent') 
    assert    contract.get_dataset(), 'valid_dataset', 'failed to set parent') 
    
def test_alias_brand(self):
    brand = 'Merck'
    contract.set_brand(brand)
    assert contract.get_brand(),
                brand,
                "brand alias not set")
    assert contract.get_child(),
                brand,
                "brand does not alias to child")
    

def test_set_partitions(self):
    partitions = ['date','segment']
    bad_partitions = ['b@d$$%Partition','good_partition_name']
    ## valid
    contract.set_partitions(partitions)
    assert contract.get_partitions(), partitions, "partitions not correctly set")

    ## invalid
    assertRaises(  ValueError,
                        lambda: contract.set_partitions(bad_partitions))
     
def test_set_file_name(self):
    good_file_name = '23598020358908325.parquet'
    bad_file_name = '@@$10-8953095830-.jpg'
    
    ## valid 
    contract.set_file_name(good_file_name)
    assert    contract.get_file_name(),
                        good_file_name,
                        "file name was not set")

    ## invalid
    assertRaises(  ValueError,
                        lambda: contract.set_file_name(bad_file_name))


def test_get_contract_type(self):
    contract = Contract(branch = 'master',
                        env = 'dev',
                        parent = 'Merck',
                        child = 'Wonder_Drug',
                        state = 'Ingest'
                        )

    ## basic
    assert    contract.get_contract_type(),
                        'state',
                        'returned wrong type for state contract')
    
    ## dataset
    contract.set_dataset('test_set')
    assert    contract.get_contract_type(),
                        'dataset',
                        'returned wrong type for dataset contract')

    ## partition
    contract.set_partitions(['test_par'])
    assert    contract.get_contract_type(),
                        'partition',
                        'returned wrong type for partition contract')

    ## file_name
    contract.set_file_name('test_file.jpg')
    assert    contract.get_contract_type(),
                        'file',
                        'returned wrong type for file contract')

    ## file_name no partition
    contract.partitions = []
    assert    contract.get_contract_type(),
                        'file',
                        'returned wrong type for file contract without partition')


def test_previous_state(self):
    contract.set_state('ingest')

    assert contract.get_previous_state(), 'Raw', 'previous state incorrect')


def test_next_state(self):
    contract.set_state('ingest')

    assert contract.get_next_state(), 'Master', 'previous state incorrect')
'''
